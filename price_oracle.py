"""
Price Oracle - Fetch real-time prices from multiple sources
"""

import requests
import time
from typing import Dict, Optional
from web3 import Web3
import json

class PriceOracle:
    def __init__(self, web3: Web3, config: dict):
        self.web3 = web3
        self.config = config
        self.cache = {}
        self.cache_ttl = config.get("cache_ttl", 60)
        
        # Uniswap V3 Quoter for onchain prices
        self.quoter_address = "0x3d4e44Eb1374240CE5F1B871ab261CD16335B76a"
        self.quoter_abi = [
            {
                "inputs": [
                    {"internalType": "address", "name": "tokenIn", "type": "address"},
                    {"internalType": "address", "name": "tokenOut", "type": "address"},
                    {"internalType": "uint24", "name": "fee", "type": "uint24"},
                    {"internalType": "uint256", "name": "amountIn", "type": "uint256"},
                    {"internalType": "uint160", "name": "sqrtPriceLimitX96", "type": "uint160"}
                ],
                "name": "quoteExactInputSingle",
                "outputs": [{"internalType": "uint256", "name": "amountOut", "type": "uint256"}],
                "stateMutability": "nonpayable",
                "type": "function"
            }
        ]
        self.quoter = web3.eth.contract(
            address=Web3.to_checksum_address(self.quoter_address),
            abi=self.quoter_abi
        )
    
    def get_price(self, token_symbol: str, vs_currency: str = "usd") -> Optional[float]:
        """Get current price with caching"""
        cache_key = f"{token_symbol}_{vs_currency}"
        
        # Check cache
        if cache_key in self.cache:
            cached_data = self.cache[cache_key]
            if time.time() - cached_data["timestamp"] < self.cache_ttl:
                return cached_data["price"]
        
        # Fetch new price
        price = None
        if self.config["primary"] == "coingecko":
            price = self._get_coingecko_price(token_symbol, vs_currency)
        
        # Fallback to onchain if primary fails
        if price is None and self.config["fallback"] == "onchain":
            price = self._get_onchain_price(token_symbol, vs_currency)
        
        # Cache result
        if price is not None:
            self.cache[cache_key] = {
                "price": price,
                "timestamp": time.time()
            }
        
        return price
    
    def _get_coingecko_price(self, token_symbol: str, vs_currency: str) -> Optional[float]:
        """Fetch price from CoinGecko (free tier)"""
        try:
            # Map symbols to CoinGecko IDs
            token_map = {
                "ETH": "ethereum",
                "WETH": "ethereum",
                "USDC": "usd-coin",
                "DAI": "dai",
                "BTC": "bitcoin"
            }
            
            token_id = token_map.get(token_symbol.upper())
            if not token_id:
                return None
            
            url = f"https://api.coingecko.com/api/v3/simple/price"
            params = {
                "ids": token_id,
                "vs_currencies": vs_currency
            }
            
            response = requests.get(url, params=params, timeout=5)
            response.raise_for_status()
            
            data = response.json()
            return data.get(token_id, {}).get(vs_currency)
            
        except Exception as e:
            print(f"CoinGecko error: {e}")
            return None
    
    def _get_onchain_price(self, token_symbol: str, vs_currency: str) -> Optional[float]:
        """Fetch price from Uniswap V3 onchain"""
        try:
            from config import TOKENS
            
            # Only support WETH/USDC for now
            if token_symbol.upper() not in ["ETH", "WETH"] or vs_currency.lower() != "usd":
                return None
            
            token_in = Web3.to_checksum_address(TOKENS["WETH"])
            token_out = Web3.to_checksum_address(TOKENS["USDC"])
            
            # Quote 1 WETH -> USDC
            amount_in = Web3.to_wei(1, 'ether')
            fee = 3000  # 0.3% fee tier
            
            # Note: quoteExactInputSingle is view function, use call()
            amount_out = self.quoter.functions.quoteExactInputSingle(
                token_in,
                token_out,
                fee,
                amount_in,
                0
            ).call()
            
            # USDC has 6 decimals
            price = amount_out / 1e6
            return price
            
        except Exception as e:
            print(f"Onchain price error: {e}")
            return None
    
    def get_historical_prices(self, token_symbol: str, days: int = 30) -> list:
        """Get historical prices for backtesting"""
        try:
            token_map = {
                "ETH": "ethereum",
                "WETH": "ethereum",
                "USDC": "usd-coin",
                "DAI": "dai"
            }
            
            token_id = token_map.get(token_symbol.upper())
            if not token_id:
                return []
            
            url = f"https://api.coingecko.com/api/v3/coins/{token_id}/market_chart"
            params = {
                "vs_currency": "usd",
                "days": days,
                "interval": "hourly"
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            prices = data.get("prices", [])
            
            # Format: [[timestamp, price], ...]
            return [{"timestamp": p[0]/1000, "price": p[1]} for p in prices]
            
        except Exception as e:
            print(f"Historical price error: {e}")
            return []
    
    def calculate_indicators(self, prices: list) -> dict:
        """Calculate technical indicators"""
        if len(prices) < 14:
            return {}
        
        # Extract price values
        price_values = [p["price"] for p in prices]
        
        # RSI (Relative Strength Index)
        rsi = self._calculate_rsi(price_values, period=14)
        
        # Moving Averages
        sma_20 = sum(price_values[-20:]) / 20 if len(price_values) >= 20 else None
        sma_50 = sum(price_values[-50:]) / 50 if len(price_values) >= 50 else None
        
        # Price change
        current_price = price_values[-1]
        price_24h_ago = price_values[-24] if len(price_values) >= 24 else price_values[0]
        change_24h = ((current_price - price_24h_ago) / price_24h_ago) * 100
        
        return {
            "rsi": rsi,
            "sma_20": sma_20,
            "sma_50": sma_50,
            "current_price": current_price,
            "change_24h": change_24h
        }
    
    def _calculate_rsi(self, prices: list, period: int = 14) -> Optional[float]:
        """Calculate RSI indicator"""
        if len(prices) < period + 1:
            return None
        
        # Calculate price changes
        changes = [prices[i] - prices[i-1] for i in range(1, len(prices))]
        
        # Separate gains and losses
        gains = [c if c > 0 else 0 for c in changes[-period:]]
        losses = [-c if c < 0 else 0 for c in changes[-period:]]
        
        # Calculate average gain and loss
        avg_gain = sum(gains) / period
        avg_loss = sum(losses) / period
        
        if avg_loss == 0:
            return 100
        
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        
        return rsi


if __name__ == "__main__":
    # Test price oracle
    from web3 import Web3
    from config import PRICE_ORACLE, BASE_RPC
    
    web3 = Web3(Web3.HTTPProvider(BASE_RPC))
    oracle = PriceOracle(web3, PRICE_ORACLE)
    
    print("=== Price Oracle Test ===\n")
    
    # Test current price
    eth_price = oracle.get_price("ETH", "usd")
    print(f"ETH Price: ${eth_price:,.2f}")
    
    # Test historical prices
    print("\nFetching historical prices (last 7 days)...")
    historical = oracle.get_historical_prices("ETH", days=7)
    print(f"Got {len(historical)} data points")
    
    # Test indicators
    if historical:
        indicators = oracle.calculate_indicators(historical)
        print(f"\nTechnical Indicators:")
        print(f"  RSI: {indicators.get('rsi', 0):.2f}")
        print(f"  SMA 20: ${indicators.get('sma_20', 0):,.2f}")
        print(f"  24h Change: {indicators.get('change_24h', 0):+.2f}%")

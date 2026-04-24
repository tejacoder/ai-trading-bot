"""
Trading Strategies
"""

from typing import Dict, Optional
import time

class Strategy:
    """Base strategy class"""
    
    def __init__(self, name: str, config: dict):
        self.name = name
        self.config = config
        self.enabled = config.get("enabled", False)
        self.last_signal_time = 0
    
    def should_trade(self, market_data: dict) -> Optional[Dict]:
        """
        Returns trade signal or None
        Signal format: {
            "action": "buy" | "sell",
            "amount": float,
            "reason": str,
            "confidence": float (0-1)
        }
        """
        raise NotImplementedError


class DCAStrategy(Strategy):
    """Dollar Cost Averaging - Buy fixed amount at regular intervals"""
    
    def __init__(self, config: dict):
        super().__init__("DCA", config)
        self.interval = config.get("interval", 3600)  # 1 hour default
        self.amount_usdc = config.get("amount_usdc", 10)
        self.token = config.get("token", "WETH")
    
    def should_trade(self, market_data: dict) -> Optional[Dict]:
        if not self.enabled:
            return None
        
        current_time = time.time()
        
        # Check if enough time has passed
        if current_time - self.last_signal_time < self.interval:
            return None
        
        self.last_signal_time = current_time
        
        return {
            "action": "buy",
            "token": self.token,
            "amount_usdc": self.amount_usdc,
            "reason": f"DCA: Regular buy every {self.interval/3600:.1f}h",
            "confidence": 1.0
        }


class MomentumStrategy(Strategy):
    """RSI-based momentum trading"""
    
    def __init__(self, config: dict):
        super().__init__("Momentum", config)
        self.rsi_period = config.get("rsi_period", 14)
        self.rsi_oversold = config.get("rsi_oversold", 30)
        self.rsi_overbought = config.get("rsi_overbought", 70)
        self.check_interval = config.get("check_interval", 300)
    
    def should_trade(self, market_data: dict) -> Optional[Dict]:
        if not self.enabled:
            return None
        
        current_time = time.time()
        
        # Rate limiting
        if current_time - self.last_signal_time < self.check_interval:
            return None
        
        indicators = market_data.get("indicators", {})
        rsi = indicators.get("rsi")
        
        if rsi is None:
            return None
        
        current_price = indicators.get("current_price", 0)
        
        # Buy signal: RSI oversold
        if rsi < self.rsi_oversold:
            self.last_signal_time = current_time
            return {
                "action": "buy",
                "token": "WETH",
                "amount_usdc": 20,  # Fixed amount for now
                "reason": f"RSI oversold: {rsi:.1f} < {self.rsi_oversold}",
                "confidence": (self.rsi_oversold - rsi) / self.rsi_oversold,
                "price": current_price
            }
        
        # Sell signal: RSI overbought
        if rsi > self.rsi_overbought:
            self.last_signal_time = current_time
            return {
                "action": "sell",
                "token": "WETH",
                "amount_percent": 0.5,  # Sell 50% of holdings
                "reason": f"RSI overbought: {rsi:.1f} > {self.rsi_overbought}",
                "confidence": (rsi - self.rsi_overbought) / (100 - self.rsi_overbought),
                "price": current_price
            }
        
        return None


class GridStrategy(Strategy):
    """Grid trading - Place buy/sell orders at regular intervals"""
    
    def __init__(self, config: dict):
        super().__init__("Grid", config)
        self.grid_levels = config.get("grid_levels", 10)
        self.price_range = config.get("price_range", 0.20)  # 20%
        self.amount_per_grid = config.get("amount_per_grid", 5)
        self.grids = []
        self.base_price = None
    
    def initialize_grids(self, current_price: float):
        """Set up grid levels"""
        self.base_price = current_price
        
        # Calculate grid spacing
        price_min = current_price * (1 - self.price_range / 2)
        price_max = current_price * (1 + self.price_range / 2)
        step = (price_max - price_min) / self.grid_levels
        
        self.grids = []
        for i in range(self.grid_levels + 1):
            price = price_min + (step * i)
            self.grids.append({
                "price": price,
                "filled": False,
                "type": "buy" if price < current_price else "sell"
            })
    
    def should_trade(self, market_data: dict) -> Optional[Dict]:
        if not self.enabled:
            return None
        
        current_price = market_data.get("indicators", {}).get("current_price")
        if not current_price:
            return None
        
        # Initialize grids if not set
        if not self.grids:
            self.initialize_grids(current_price)
            return None
        
        # Check if price crossed any grid level
        for grid in self.grids:
            if grid["filled"]:
                continue
            
            # Buy grid triggered
            if grid["type"] == "buy" and current_price <= grid["price"]:
                grid["filled"] = True
                return {
                    "action": "buy",
                    "token": "WETH",
                    "amount_usdc": self.amount_per_grid,
                    "reason": f"Grid buy at ${grid['price']:.2f}",
                    "confidence": 0.8,
                    "price": current_price
                }
            
            # Sell grid triggered
            if grid["type"] == "sell" and current_price >= grid["price"]:
                grid["filled"] = True
                return {
                    "action": "sell",
                    "token": "WETH",
                    "amount_percent": 0.1,  # Sell 10% per grid
                    "reason": f"Grid sell at ${grid['price']:.2f}",
                    "confidence": 0.8,
                    "price": current_price
                }
        
        return None


class ArbitrageStrategy(Strategy):
    """Cross-DEX arbitrage"""
    
    def __init__(self, config: dict):
        super().__init__("Arbitrage", config)
        self.min_profit = config.get("min_profit", 0.005)  # 0.5%
        self.check_interval = config.get("check_interval", 60)
    
    def should_trade(self, market_data: dict) -> Optional[Dict]:
        if not self.enabled:
            return None
        
        # TODO: Implement cross-DEX price comparison
        # For now, return None
        return None


class StrategyManager:
    """Manage multiple strategies"""
    
    def __init__(self, strategies_config: dict):
        self.strategies = []
        
        # Initialize enabled strategies
        if strategies_config.get("dca", {}).get("enabled"):
            self.strategies.append(DCAStrategy(strategies_config["dca"]))
        
        if strategies_config.get("momentum", {}).get("enabled"):
            self.strategies.append(MomentumStrategy(strategies_config["momentum"]))
        
        if strategies_config.get("grid", {}).get("enabled"):
            self.strategies.append(GridStrategy(strategies_config["grid"]))
        
        if strategies_config.get("arbitrage", {}).get("enabled"):
            self.strategies.append(ArbitrageStrategy(strategies_config["arbitrage"]))
    
    def get_signals(self, market_data: dict) -> list:
        """Get trade signals from all strategies"""
        signals = []
        
        for strategy in self.strategies:
            signal = strategy.should_trade(market_data)
            if signal:
                signal["strategy"] = strategy.name
                signals.append(signal)
        
        return signals
    
    def get_best_signal(self, market_data: dict) -> Optional[Dict]:
        """Get highest confidence signal"""
        signals = self.get_signals(market_data)
        
        if not signals:
            return None
        
        # Sort by confidence
        signals.sort(key=lambda x: x.get("confidence", 0), reverse=True)
        
        return signals[0]


if __name__ == "__main__":
    # Test strategies
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from config import STRATEGIES
    
    manager = StrategyManager(STRATEGIES)
    
    print(f"=== Strategy Manager Test ===\n")
    print(f"Active strategies: {len(manager.strategies)}")
    for s in manager.strategies:
        print(f"  - {s.name}")
    
    # Test with mock data
    mock_data = {
        "indicators": {
            "rsi": 25,  # Oversold
            "current_price": 2850,
            "sma_20": 2900,
            "change_24h": -5.2
        }
    }
    
    print(f"\nMock market data:")
    print(f"  Price: ${mock_data['indicators']['current_price']}")
    print(f"  RSI: {mock_data['indicators']['rsi']}")
    
    signal = manager.get_best_signal(mock_data)
    if signal:
        print(f"\nTrade signal generated:")
        print(f"  Strategy: {signal['strategy']}")
        print(f"  Action: {signal['action'].upper()}")
        print(f"  Reason: {signal['reason']}")
        print(f"  Confidence: {signal['confidence']:.1%}")
    else:
        print(f"\nNo trade signals")

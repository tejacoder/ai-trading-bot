"""
Trading Bot - Main execution engine
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from web3 import Web3
import json
import time
from datetime import datetime
from wallet_adapter import TradingBotWallet
from price_oracle import PriceOracle
from strategies.trading_strategies import StrategyManager
from risk_manager import RiskManager
import config

class TradingBot:
    def __init__(self, password: str = None):
        print("🤖 Initializing Trading Bot...")
        
        # Load configuration
        self.config = config
        self.dry_run = config.SAFETY["dry_run"]
        self.require_confirmation = config.SAFETY["require_confirmation"]
        
        # Initialize Web3
        self.web3 = Web3(Web3.HTTPProvider(config.BASE_RPC))
        if not self.web3.is_connected():
            raise Exception("Failed to connect to Base RPC")
        
        # Initialize wallet (auto-detects encrypted/plaintext)
        self.wallet = TradingBotWallet(password=password)
        self.wallet.load()
        
        print(f"  Wallet: {self.wallet.address}")
        print(f"  Type: {'Encrypted' if self.wallet._is_encrypted else 'Plaintext'}")
        print(f"  Builder Code: {config.BUILDER_CODE}")
        
        # Initialize components
        self.oracle = PriceOracle(self.web3, config.PRICE_ORACLE)
        self.strategy_manager = StrategyManager(config.STRATEGIES)
        self.risk_manager = RiskManager(config.RISK_CONFIG)
        
        # State
        self.running = False
        self.portfolio = {}
        self.trade_history = []
        
        print(f"  Strategies: {len(self.strategy_manager.strategies)}")
        for s in self.strategy_manager.strategies:
            print(f"    - {s.name}")
        
        print(f"  Mode: {'DRY RUN' if self.dry_run else 'LIVE TRADING'}")
        print()
    
    def get_portfolio(self) -> dict:
        """Get current portfolio state"""
        
        # Get ETH balance
        eth_balance = self.wallet.get_balance()
        
        # Get token balances
        usdc_balance = self.wallet.get_token_balance(config.TOKENS["USDC"])
        
        # Get current prices
        eth_price = self.oracle.get_price("ETH", "usd")
        
        # Calculate total value
        eth_value = eth_balance * eth_price if eth_price else 0
        usdc_value = usdc_balance
        total_value = eth_value + usdc_value
        
        return {
            "timestamp": time.time(),
            "eth_balance": eth_balance,
            "usdc_balance": usdc_balance,
            "eth_price": eth_price,
            "eth_value_usd": eth_value,
            "usdc_value_usd": usdc_value,
            "total_value_usd": total_value,
            "tokens": {
                "WETH": eth_balance,
                "USDC": usdc_balance
            }
        }
    
    def get_market_data(self) -> dict:
        """Get current market data with indicators"""
        
        # Get current price
        current_price = self.oracle.get_price("ETH", "usd")
        
        # Get historical data for indicators
        historical = self.oracle.get_historical_prices("ETH", days=7)
        
        # Calculate indicators
        indicators = self.oracle.calculate_indicators(historical)
        
        return {
            "timestamp": time.time(),
            "current_price": current_price,
            "historical": historical,
            "indicators": indicators
        }
    
    def execute_trade(self, signal: dict) -> dict:
        """Execute a trade signal"""
        
        print(f"\n{'='*60}")
        print(f"📊 TRADE SIGNAL")
        print(f"{'='*60}")
        print(f"Strategy: {signal.get('strategy', 'Unknown')}")
        print(f"Action: {signal['action'].upper()}")
        print(f"Token: {signal.get('token', 'WETH')}")
        print(f"Reason: {signal['reason']}")
        print(f"Confidence: {signal.get('confidence', 0):.1%}")
        
        if signal.get('price'):
            print(f"Price: ${signal['price']:,.2f}")
        
        # Calculate position size
        position_size = self.risk_manager.calculate_position_size(signal, self.portfolio)
        
        if signal["action"] == "buy":
            print(f"Amount: ${position_size:.2f} USDC")
        else:
            print(f"Amount: {position_size:.6f} {signal.get('token', 'WETH')}")
        
        # Dry run check
        if self.dry_run:
            print(f"\n⚠️  DRY RUN MODE - Trade not executed")
            print(f"{'='*60}\n")
            return {
                "success": True,
                "dry_run": True,
                "signal": signal
            }
        
        # Confirmation check
        if self.require_confirmation:
            response = input(f"\nExecute this trade? (yes/no): ").strip().lower()
            if response != "yes":
                print(f"❌ Trade cancelled by user")
                print(f"{'='*60}\n")
                return {
                    "success": False,
                    "cancelled": True
                }
        
        # Execute trade
        try:
            if signal["action"] == "buy":
                # Buy token with USDC
                print(f"\n🔄 Executing buy...")
                
                token = signal.get("token", "WETH")
                amount_usdc = position_size
                
                # Use wallet's swap function (includes builder code!)
                tx_hash = self.wallet.swap_tokens(
                    from_token="USDC",
                    to_token=token,
                    amount=amount_usdc
                )
                
                print(f"✅ Buy executed")
                print(f"   TX: {tx_hash}")
                print(f"   Builder code: {config.BUILDER_CODE} ✅")
                
                result = {
                    "success": True,
                    "action": "buy",
                    "token": token,
                    "amount": position_size,
                    "price": signal.get("price", 0),
                    "tx_hash": tx_hash,
                    "timestamp": time.time(),
                    "builder_code": config.BUILDER_CODE
                }
            
            elif signal["action"] == "sell":
                # Sell token for USDC
                print(f"\n🔄 Executing sell...")
                
                token = signal.get("token", "WETH")
                amount_token = position_size
                
                # Use wallet's swap function (includes builder code!)
                tx_hash = self.wallet.swap_tokens(
                    from_token=token,
                    to_token="USDC",
                    amount=amount_token
                )
                
                print(f"✅ Sell executed")
                print(f"   TX: {tx_hash}")
                print(f"   Builder code: {config.BUILDER_CODE} ✅")
                
                result = {
                    "success": True,
                    "action": "sell",
                    "token": token,
                    "amount": position_size,
                    "price": signal.get("price", 0),
                    "tx_hash": tx_hash,
                    "timestamp": time.time(),
                    "builder_code": config.BUILDER_CODE
                }
            
            # Record trade
            self.risk_manager.record_trade(result)
            self.trade_history.append(result)
            
            print(f"{'='*60}\n")
            return result
            
        except Exception as e:
            print(f"❌ Trade failed: {e}")
            print(f"{'='*60}\n")
            return {
                "success": False,
                "error": str(e)
            }
    
    def run_cycle(self):
        """Run one trading cycle"""
        
        print(f"\n{'─'*60}")
        print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'─'*60}")
        
        # Update portfolio
        self.portfolio = self.get_portfolio()
        
        print(f"\n💼 Portfolio:")
        print(f"   ETH: {self.portfolio['eth_balance']:.6f} (${self.portfolio['eth_value_usd']:.2f})")
        print(f"   USDC: ${self.portfolio['usdc_balance']:.2f}")
        print(f"   Total: ${self.portfolio['total_value_usd']:.2f}")
        
        # Get market data
        market_data = self.get_market_data()
        
        print(f"\n📈 Market:")
        print(f"   ETH Price: ${market_data['current_price']:,.2f}")
        
        if market_data['indicators']:
            ind = market_data['indicators']
            print(f"   RSI: {ind.get('rsi', 0):.1f}")
            print(f"   24h Change: {ind.get('change_24h', 0):+.2f}%")
        
        # Check stop-loss / take-profit
        current_prices = {"WETH": market_data['current_price']}
        
        sl_signals = self.risk_manager.check_stop_loss(self.portfolio, current_prices)
        tp_signals = self.risk_manager.check_take_profit(self.portfolio, current_prices)
        
        # Priority: stop-loss > take-profit > strategy signals
        if sl_signals:
            signal = sl_signals[0]
            print(f"\n🚨 Stop-loss triggered!")
        elif tp_signals:
            signal = tp_signals[0]
            print(f"\n🎯 Take-profit triggered!")
        else:
            # Get strategy signal
            signal = self.strategy_manager.get_best_signal(market_data)
        
        if signal:
            # Risk check
            can_trade, reason = self.risk_manager.can_trade(signal, self.portfolio)
            
            if can_trade:
                self.execute_trade(signal)
            else:
                print(f"\n⚠️  Trade blocked: {reason}")
        else:
            print(f"\n💤 No trade signals")
        
        # Show risk stats
        stats = self.risk_manager.get_stats()
        print(f"\n📊 Risk Stats:")
        print(f"   Daily trades: {stats['daily_trades']}/{stats['max_daily_trades']}")
        print(f"   Open positions: {stats['open_positions']}")
    
    def start(self, interval: int = 300):
        """Start trading bot"""
        
        print(f"\n{'='*60}")
        print(f"🚀 TRADING BOT STARTED")
        print(f"{'='*60}")
        print(f"Check interval: {interval}s ({interval/60:.1f} minutes)")
        print(f"Press Ctrl+C to stop")
        print(f"{'='*60}\n")
        
        self.running = True
        
        try:
            while self.running:
                self.run_cycle()
                
                # Wait for next cycle
                print(f"\n⏳ Next check in {interval}s...")
                time.sleep(interval)
        
        except KeyboardInterrupt:
            print(f"\n\n{'='*60}")
            print(f"🛑 TRADING BOT STOPPED")
            print(f"{'='*60}")
            print(f"Total trades: {len(self.trade_history)}")
            print(f"{'='*60}\n")
            self.running = False
    
    def backtest(self, days: int = 30):
        """Run backtest on historical data"""
        
        print(f"\n{'='*60}")
        print(f"📊 BACKTESTING - Last {days} days")
        print(f"{'='*60}\n")
        
        # Get historical data
        print(f"Fetching historical data...")
        historical = self.oracle.get_historical_prices("ETH", days=days)
        
        if not historical:
            print(f"❌ No historical data available")
            return
        
        print(f"Got {len(historical)} data points")
        
        # Initialize backtest state
        initial_capital = config.BACKTEST_CONFIG["initial_capital"]
        usdc_balance = initial_capital
        eth_balance = 0
        trades = []
        
        print(f"Initial capital: ${initial_capital:.2f} USDC\n")
        
        # Simulate trading
        for i in range(14, len(historical)):  # Need 14 points for RSI
            # Get price window
            price_window = historical[max(0, i-50):i+1]
            
            # Calculate indicators
            indicators = self.oracle.calculate_indicators(price_window)
            current_price = indicators["current_price"]
            
            # Get signal
            market_data = {"indicators": indicators}
            signal = self.strategy_manager.get_best_signal(market_data)
            
            if not signal:
                continue
            
            # Execute simulated trade
            if signal["action"] == "buy" and usdc_balance > 0:
                amount_usdc = min(signal.get("amount_usdc", 10), usdc_balance)
                eth_bought = amount_usdc / current_price
                
                usdc_balance -= amount_usdc
                eth_balance += eth_bought
                
                trades.append({
                    "timestamp": price_window[-1]["timestamp"],
                    "action": "buy",
                    "price": current_price,
                    "amount_usdc": amount_usdc,
                    "eth_amount": eth_bought
                })
                
                print(f"BUY  @ ${current_price:,.2f} | {eth_bought:.6f} ETH | {signal['reason']}")
            
            elif signal["action"] == "sell" and eth_balance > 0:
                amount_eth = eth_balance * signal.get("amount_percent", 1.0)
                usdc_received = amount_eth * current_price
                
                eth_balance -= amount_eth
                usdc_balance += usdc_received
                
                trades.append({
                    "timestamp": price_window[-1]["timestamp"],
                    "action": "sell",
                    "price": current_price,
                    "amount_usdc": usdc_received,
                    "eth_amount": amount_eth
                })
                
                print(f"SELL @ ${current_price:,.2f} | {amount_eth:.6f} ETH | {signal['reason']}")
        
        # Calculate final value
        final_price = historical[-1]["price"]
        final_value = usdc_balance + (eth_balance * final_price)
        profit = final_value - initial_capital
        profit_pct = (profit / initial_capital) * 100
        
        # Calculate buy & hold
        buy_hold_eth = initial_capital / historical[0]["price"]
        buy_hold_value = buy_hold_eth * final_price
        buy_hold_profit = buy_hold_value - initial_capital
        buy_hold_pct = (buy_hold_profit / initial_capital) * 100
        
        print(f"\n{'='*60}")
        print(f"📊 BACKTEST RESULTS")
        print(f"{'='*60}")
        print(f"Initial capital: ${initial_capital:.2f}")
        print(f"Final value: ${final_value:.2f}")
        print(f"Profit: ${profit:+.2f} ({profit_pct:+.2f}%)")
        print(f"\nTotal trades: {len(trades)}")
        print(f"Final holdings:")
        print(f"  USDC: ${usdc_balance:.2f}")
        print(f"  ETH: {eth_balance:.6f} (${eth_balance * final_price:.2f})")
        print(f"\nBuy & Hold comparison:")
        print(f"  Value: ${buy_hold_value:.2f}")
        print(f"  Profit: ${buy_hold_profit:+.2f} ({buy_hold_pct:+.2f}%)")
        print(f"  Strategy vs B&H: {profit_pct - buy_hold_pct:+.2f}%")
        print(f"{'='*60}\n")


if __name__ == "__main__":
    import sys
    import os
    
    # Get password from environment or prompt
    password = os.getenv('WALLET_PASSWORD')
    
    bot = TradingBot(password=password)
    
    if len(sys.argv) > 1 and sys.argv[1] == "backtest":
        # Run backtest
        days = int(sys.argv[2]) if len(sys.argv) > 2 else 30
        bot.backtest(days=days)
    else:
        # Run live bot
        interval = int(sys.argv[1]) if len(sys.argv) > 1 else 300
        bot.start(interval=interval)

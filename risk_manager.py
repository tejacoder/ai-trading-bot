"""
Risk Manager - Handle position sizing, stop-loss, take-profit
"""

from typing import Dict, Optional
import time

class RiskManager:
    def __init__(self, config: dict):
        self.config = config
        self.max_position_size = config.get("max_position_size", 0.1)
        self.max_slippage = config.get("max_slippage", 0.01)
        self.stop_loss = config.get("stop_loss", 0.05)
        self.take_profit = config.get("take_profit", 0.10)
        self.max_daily_trades = config.get("max_daily_trades", 20)
        self.min_profit_threshold = config.get("min_profit_threshold", 0.02)
        
        # Track trades
        self.daily_trades = []
        self.positions = {}  # token -> {entry_price, amount, timestamp}
    
    def can_trade(self, signal: dict, portfolio: dict) -> tuple[bool, str]:
        """Check if trade passes risk checks"""
        
        # Check daily trade limit
        current_day = time.strftime("%Y-%m-%d")
        today_trades = [t for t in self.daily_trades if t["date"] == current_day]
        
        if len(today_trades) >= self.max_daily_trades:
            return False, f"Daily trade limit reached ({self.max_daily_trades})"
        
        # Check position size
        if signal["action"] == "buy":
            total_value = portfolio.get("total_value_usd", 0)
            trade_value = signal.get("amount_usdc", 0)
            
            if total_value > 0:
                position_size = trade_value / total_value
                if position_size > self.max_position_size:
                    return False, f"Position size too large: {position_size:.1%} > {self.max_position_size:.1%}"
        
        # Check minimum profit threshold for sell signals
        if signal["action"] == "sell":
            token = signal.get("token", "WETH")
            position = self.positions.get(token)
            
            if position:
                current_price = signal.get("price", 0)
                entry_price = position["entry_price"]
                profit_pct = (current_price - entry_price) / entry_price
                
                if profit_pct < self.min_profit_threshold:
                    return False, f"Profit too low: {profit_pct:.1%} < {self.min_profit_threshold:.1%}"
        
        return True, "OK"
    
    def calculate_position_size(self, signal: dict, portfolio: dict) -> float:
        """Calculate safe position size"""
        
        if signal["action"] == "buy":
            total_value = portfolio.get("total_value_usd", 0)
            max_trade_value = total_value * self.max_position_size
            
            requested_amount = signal.get("amount_usdc", 0)
            
            # Use smaller of requested or max allowed
            return min(requested_amount, max_trade_value)
        
        elif signal["action"] == "sell":
            token = signal.get("token", "WETH")
            token_balance = portfolio.get("tokens", {}).get(token, 0)
            
            # If amount_percent specified, use that
            if "amount_percent" in signal:
                return token_balance * signal["amount_percent"]
            
            # Otherwise sell all
            return token_balance
        
        return 0
    
    def check_stop_loss(self, portfolio: dict, current_prices: dict) -> list:
        """Check if any positions hit stop-loss"""
        signals = []
        
        for token, position in self.positions.items():
            current_price = current_prices.get(token)
            if not current_price:
                continue
            
            entry_price = position["entry_price"]
            loss_pct = (current_price - entry_price) / entry_price
            
            if loss_pct <= -self.stop_loss:
                signals.append({
                    "action": "sell",
                    "token": token,
                    "amount_percent": 1.0,  # Sell all
                    "reason": f"Stop-loss triggered: {loss_pct:.1%}",
                    "confidence": 1.0,
                    "price": current_price,
                    "strategy": "RiskManager"
                })
        
        return signals
    
    def check_take_profit(self, portfolio: dict, current_prices: dict) -> list:
        """Check if any positions hit take-profit"""
        signals = []
        
        for token, position in self.positions.items():
            current_price = current_prices.get(token)
            if not current_price:
                continue
            
            entry_price = position["entry_price"]
            profit_pct = (current_price - entry_price) / entry_price
            
            if profit_pct >= self.take_profit:
                signals.append({
                    "action": "sell",
                    "token": token,
                    "amount_percent": 0.5,  # Sell half
                    "reason": f"Take-profit triggered: {profit_pct:.1%}",
                    "confidence": 1.0,
                    "price": current_price,
                    "strategy": "RiskManager"
                })
        
        return signals
    
    def record_trade(self, trade: dict):
        """Record executed trade"""
        trade["date"] = time.strftime("%Y-%m-%d")
        trade["timestamp"] = time.time()
        self.daily_trades.append(trade)
        
        # Update positions
        token = trade.get("token", "WETH")
        
        if trade["action"] == "buy":
            if token not in self.positions:
                self.positions[token] = {
                    "entry_price": trade["price"],
                    "amount": trade["amount"],
                    "timestamp": trade["timestamp"]
                }
            else:
                # Average down
                pos = self.positions[token]
                total_amount = pos["amount"] + trade["amount"]
                avg_price = (pos["entry_price"] * pos["amount"] + trade["price"] * trade["amount"]) / total_amount
                pos["entry_price"] = avg_price
                pos["amount"] = total_amount
        
        elif trade["action"] == "sell":
            if token in self.positions:
                pos = self.positions[token]
                pos["amount"] -= trade["amount"]
                
                # Remove position if fully sold
                if pos["amount"] <= 0:
                    del self.positions[token]
    
    def get_stats(self) -> dict:
        """Get risk management statistics"""
        current_day = time.strftime("%Y-%m-%d")
        today_trades = [t for t in self.daily_trades if t["date"] == current_day]
        
        return {
            "daily_trades": len(today_trades),
            "max_daily_trades": self.max_daily_trades,
            "open_positions": len(self.positions),
            "positions": self.positions
        }


if __name__ == "__main__":
    # Test risk manager
    from config import RISK_CONFIG
    
    risk_mgr = RiskManager(RISK_CONFIG)
    
    print("=== Risk Manager Test ===\n")
    print(f"Configuration:")
    print(f"  Max position size: {risk_mgr.max_position_size:.1%}")
    print(f"  Stop loss: {risk_mgr.stop_loss:.1%}")
    print(f"  Take profit: {risk_mgr.take_profit:.1%}")
    print(f"  Max daily trades: {risk_mgr.max_daily_trades}")
    
    # Test buy signal
    mock_signal = {
        "action": "buy",
        "token": "WETH",
        "amount_usdc": 50,
        "price": 2850
    }
    
    mock_portfolio = {
        "total_value_usd": 1000,
        "tokens": {"WETH": 0.1}
    }
    
    can_trade, reason = risk_mgr.can_trade(mock_signal, mock_portfolio)
    print(f"\nBuy signal check: {can_trade}")
    print(f"  Reason: {reason}")
    
    if can_trade:
        position_size = risk_mgr.calculate_position_size(mock_signal, mock_portfolio)
        print(f"  Position size: ${position_size:.2f}")
    
    # Test stop-loss
    risk_mgr.positions["WETH"] = {
        "entry_price": 3000,
        "amount": 0.1,
        "timestamp": time.time()
    }
    
    current_prices = {"WETH": 2700}  # 10% loss
    
    stop_loss_signals = risk_mgr.check_stop_loss(mock_portfolio, current_prices)
    if stop_loss_signals:
        print(f"\nStop-loss triggered:")
        for sig in stop_loss_signals:
            print(f"  {sig['reason']}")

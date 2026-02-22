"""
Strategies Module - Trading strategy implementations.
These are strategy selector classes that work with the backtester.
"""

from typing import List, Dict, Optional, Any
from dataclasses import dataclass, field


@dataclass
class KeyLevelsStrategy:
    """Trade predefined support/resistance levels."""
    name: str
    description: str = "Trade predefined S/R levels"
    rules: Dict[str, Any] = field(default_factory=dict)
    trades: List = field(default_factory=list)
    
    def __post_init__(self):
        self.key_levels = {
            'USDJPY': [
                {'level': 156.025, 'direction': 'Sell', 'confidence': 1.0},
                {'level': 154.950, 'direction': 'Buy', 'confidence': 0.8},
            ],
            'EURUSD': [
                {'level': 1.15980, 'direction': 'Buy', 'confidence': 1.0},
                {'level': 1.17215, 'direction': 'Buy', 'confidence': 0.8},
            ],
            'XAUUSD': [
                {'level': 4200, 'direction': 'Buy', 'confidence': 0.8},
                {'level': 4221, 'direction': 'Sell', 'confidence': 0.8},
                {'level': 4247, 'direction': 'Buy', 'confidence': 0.9},
                {'level': 4323, 'direction': 'Buy', 'confidence': 0.9},
                {'level': 4405, 'direction': 'Buy', 'confidence': 0.8},
            ],
            'EURAUD': [
                {'level': 1.7745, 'direction': 'Sell', 'confidence': 1.0},
                {'level': 1.7747, 'direction': 'Sell', 'confidence': 1.0},
            ],
            'AUDCAD': [
                {'level': 0.91620, 'direction': 'Buy', 'confidence': 1.0},
            ],
            'GBPNZD': [
                {'level': 2.29990, 'direction': 'Buy', 'confidence': 1.0},
            ],
            'GBPJPY': [
                {'level': 205.840, 'direction': 'Buy', 'confidence': 0.8},
            ],
            'USDCHF': [
                {'level': 0.80815, 'direction': 'Sell', 'confidence': 1.0},
                {'level': 0.79460, 'direction': 'Sell', 'confidence': 0.8},
            ],
        }
    
    def should_take_trade(self, trade) -> bool:
        pair = trade.pair
        entry = trade.entry
        direction = trade.direction
        
        if pair not in self.key_levels or entry is None:
            return False
        
        for level_info in self.key_levels[pair]:
            level = level_info['level']
            tolerance = self._get_tolerance(pair)
            
            if abs(entry - level) <= tolerance:
                if direction == level_info['direction']:
                    return True
        return False
    
    def _get_tolerance(self, pair: str) -> float:
        if pair == 'XAUUSD':
            return 5.0
        elif 'JPY' in pair:
            return 0.05
        return 0.0005
    
    def add_trade(self, trade):
        trade.strategy = self.name
        self.trades.append(trade)
    
    def calculate_winrate(self, exclude_pending: bool = True) -> float:
        if not self.trades:
            return 0.0
        trades_to_count = [t for t in self.trades if t.result != 'pending'] if exclude_pending else self.trades
        if not trades_to_count:
            return 0.0
        winners = len([t for t in trades_to_count if t.result == 'win'])
        return (winners / len(trades_to_count)) * 100
    
    def total_pips(self) -> float:
        return sum(t.pips for t in self.trades if t.result != 'pending')
    
    def total_trades(self) -> int:
        return len(self.trades)
    
    def wins(self) -> int:
        return len([t for t in self.trades if t.result == 'win'])
    
    def losses(self) -> int:
        return len([t for t in self.trades if t.result == 'loss'])
    
    def breakevens(self) -> int:
        return len([t for t in self.trades if t.result == 'breakeven'])
    
    def profit_factor(self) -> float:
        gross_profit = sum(t.pips for t in self.trades if t.pips > 0)
        gross_loss = abs(sum(t.pips for t in self.trades if t.pips < 0))
        if gross_loss == 0:
            return gross_profit if gross_profit > 0 else 1.0
        return gross_profit / gross_loss
    
    def by_pair(self) -> Dict[str, List]:
        result = {}
        for trade in self.trades:
            if trade.pair not in result:
                result[trade.pair] = []
            result[trade.pair].append(trade)
        return result
    
    def to_dict(self) -> Dict:
        completed = [t for t in self.trades if t.result != 'pending']
        return {
            'name': self.name,
            'description': self.description,
            'total_trades': self.total_trades(),
            'completed_trades': len(completed),
            'wins': self.wins(),
            'losses': self.losses(),
            'breakevens': self.breakevens(),
            'win_rate': round(self.calculate_winrate(), 2),
            'total_pips': round(self.total_pips(), 2),
            'profit_factor': round(self.profit_factor(), 2),
        }


@dataclass
class GoldMeanReversionStrategy:
    """Buy dips and sell rips on XAUUSD."""
    name: str
    description: str = "Buy dips/sell rips on XAUUSD"
    rules: Dict[str, Any] = field(default_factory=dict)
    trades: List = field(default_factory=list)
    
    def __post_init__(self):
        self.gold_ranges = [
            {'low': 4175, 'high': 4190, 'action': 'Buy'},
            {'low': 4190, 'high': 4205, 'action': 'Buy'},
            {'low': 4205, 'high': 4215, 'action': 'Both'},
            {'low': 4215, 'high': 4225, 'action': 'Sell'},
            {'low': 4225, 'high': 4250, 'action': 'Sell'},
            {'low': 4250, 'high': 4350, 'action': 'Buy'},  # Breakout zone
            {'low': 4350, 'high': 4500, 'action': 'Buy'},  # Trend continuation
        ]
    
    def should_take_trade(self, trade) -> bool:
        if trade.pair != 'XAUUSD':
            return False
        entry = trade.entry
        direction = trade.direction
        
        if entry is None:
            return False
        
        for range_info in self.gold_ranges:
            if range_info['low'] <= entry <= range_info['high']:
                if range_info['action'] == 'Both':
                    return True
                elif range_info['action'] == direction:
                    return True
        return False
    
    def add_trade(self, trade):
        trade.strategy = self.name
        self.trades.append(trade)
    
    def calculate_winrate(self, exclude_pending: bool = True) -> float:
        if not self.trades:
            return 0.0
        trades_to_count = [t for t in self.trades if t.result != 'pending'] if exclude_pending else self.trades
        if not trades_to_count:
            return 0.0
        winners = len([t for t in trades_to_count if t.result == 'win'])
        return (winners / len(trades_to_count)) * 100
    
    def total_pips(self) -> float:
        return sum(t.pips for t in self.trades if t.result != 'pending')
    
    def total_trades(self) -> int:
        return len(self.trades)
    
    def wins(self) -> int:
        return len([t for t in self.trades if t.result == 'win'])
    
    def losses(self) -> int:
        return len([t for t in self.trades if t.result == 'loss'])
    
    def breakevens(self) -> int:
        return len([t for t in self.trades if t.result == 'breakeven'])
    
    def profit_factor(self) -> float:
        gross_profit = sum(t.pips for t in self.trades if t.pips > 0)
        gross_loss = abs(sum(t.pips for t in self.trades if t.pips < 0))
        if gross_loss == 0:
            return gross_profit if gross_profit > 0 else 1.0
        return gross_profit / gross_loss
    
    def by_pair(self) -> Dict[str, List]:
        result = {}
        for trade in self.trades:
            if trade.pair not in result:
                result[trade.pair] = []
            result[trade.pair].append(trade)
        return result
    
    def to_dict(self) -> Dict:
        completed = [t for t in self.trades if t.result != 'pending']
        return {
            'name': self.name,
            'description': self.description,
            'total_trades': self.total_trades(),
            'completed_trades': len(completed),
            'wins': self.wins(),
            'losses': self.losses(),
            'breakevens': self.breakevens(),
            'win_rate': round(self.calculate_winrate(), 2),
            'total_pips': round(self.total_pips(), 2),
            'profit_factor': round(self.profit_factor(), 2),
        }


@dataclass
class TrendFollowingStrategy:
    """Hold for TP3 in trending markets."""
    name: str
    description: str = "Hold for TP3 in trending markets"
    rules: Dict[str, Any] = field(default_factory=dict)
    trades: List = field(default_factory=list)
    
    def should_take_trade(self, trade) -> bool:
        condition = trade.market_condition.lower() if hasattr(trade, 'market_condition') else 'unknown'
        # In trending markets, take all trades
        if condition == 'trending':
            return True
        elif condition == 'mixed':
            # Only take if has TP3 potential
            if trade.tp3 is not None:
                return True
        return False
    
    def add_trade(self, trade):
        trade.strategy = self.name
        self.trades.append(trade)
    
    def calculate_winrate(self, exclude_pending: bool = True) -> float:
        if not self.trades:
            return 0.0
        trades_to_count = [t for t in self.trades if t.result != 'pending'] if exclude_pending else self.trades
        if not trades_to_count:
            return 0.0
        winners = len([t for t in trades_to_count if t.result == 'win'])
        return (winners / len(trades_to_count)) * 100
    
    def total_pips(self) -> float:
        return sum(t.pips for t in self.trades if t.result != 'pending')
    
    def total_trades(self) -> int:
        return len(self.trades)
    
    def wins(self) -> int:
        return len([t for t in self.trades if t.result == 'win'])
    
    def losses(self) -> int:
        return len([t for t in self.trades if t.result == 'loss'])
    
    def breakevens(self) -> int:
        return len([t for t in self.trades if t.result == 'breakeven'])
    
    def profit_factor(self) -> float:
        gross_profit = sum(t.pips for t in self.trades if t.pips > 0)
        gross_loss = abs(sum(t.pips for t in self.trades if t.pips < 0))
        if gross_loss == 0:
            return gross_profit if gross_profit > 0 else 1.0
        return gross_profit / gross_loss
    
    def by_pair(self) -> Dict[str, List]:
        result = {}
        for trade in self.trades:
            if trade.pair not in result:
                result[trade.pair] = []
            result[trade.pair].append(trade)
        return result
    
    def to_dict(self) -> Dict:
        completed = [t for t in self.trades if t.result != 'pending']
        return {
            'name': self.name,
            'description': self.description,
            'total_trades': self.total_trades(),
            'completed_trades': len(completed),
            'wins': self.wins(),
            'losses': self.losses(),
            'breakevens': self.breakevens(),
            'win_rate': round(self.calculate_winrate(), 2),
            'total_pips': round(self.total_pips(), 2),
            'profit_factor': round(self.profit_factor(), 2),
        }


@dataclass
class MultiDayHoldStrategy:
    """1-3 day swing trades."""
    name: str
    description: str = "1-3 day swing trades"
    rules: Dict[str, Any] = field(default_factory=dict)
    trades: List = field(default_factory=list)
    
    def __post_init__(self):
        self.swing_pairs = ['EURAUD', 'AUDCAD', 'GBPNZD', 'GBPJPY', 'EURNZD']
    
    def should_take_trade(self, trade) -> bool:
        # Focus on pairs that historically show multi-day moves
        if trade.pair in self.swing_pairs:
            return True
        # Any trade with TP3 >= 100 pips is a swing candidate
        if trade.tp3 is not None:
            if trade.pair == 'XAUUSD':
                pips = abs(trade.tp3 - trade.entry)
            elif 'JPY' in trade.pair:
                pips = abs(trade.tp3 - trade.entry) * 100
            else:
                pips = abs(trade.tp3 - trade.entry) * 10000
            if pips >= 80:
                return True
        return False
    
    def add_trade(self, trade):
        trade.strategy = self.name
        self.trades.append(trade)
    
    def calculate_winrate(self, exclude_pending: bool = True) -> float:
        if not self.trades:
            return 0.0
        trades_to_count = [t for t in self.trades if t.result != 'pending'] if exclude_pending else self.trades
        if not trades_to_count:
            return 0.0
        winners = len([t for t in trades_to_count if t.result == 'win'])
        return (winners / len(trades_to_count)) * 100
    
    def total_pips(self) -> float:
        return sum(t.pips for t in self.trades if t.result != 'pending')
    
    def total_trades(self) -> int:
        return len(self.trades)
    
    def wins(self) -> int:
        return len([t for t in self.trades if t.result == 'win'])
    
    def losses(self) -> int:
        return len([t for t in self.trades if t.result == 'loss'])
    
    def breakevens(self) -> int:
        return len([t for t in self.trades if t.result == 'breakeven'])
    
    def profit_factor(self) -> float:
        gross_profit = sum(t.pips for t in self.trades if t.pips > 0)
        gross_loss = abs(sum(t.pips for t in self.trades if t.pips < 0))
        if gross_loss == 0:
            return gross_profit if gross_profit > 0 else 1.0
        return gross_profit / gross_loss
    
    def by_pair(self) -> Dict[str, List]:
        result = {}
        for trade in self.trades:
            if trade.pair not in result:
                result[trade.pair] = []
            result[trade.pair].append(trade)
        return result
    
    def to_dict(self) -> Dict:
        completed = [t for t in self.trades if t.result != 'pending']
        return {
            'name': self.name,
            'description': self.description,
            'total_trades': self.total_trades(),
            'completed_trades': len(completed),
            'wins': self.wins(),
            'losses': self.losses(),
            'breakevens': self.breakevens(),
            'win_rate': round(self.calculate_winrate(), 2),
            'total_pips': round(self.total_pips(), 2),
            'profit_factor': round(self.profit_factor(), 2),
        }

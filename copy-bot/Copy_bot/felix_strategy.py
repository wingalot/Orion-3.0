"""
Felix Strategy Module - Replicates the original Felix VIP approach.

Key characteristics identified from analysis:
1. Dynamic SL: -80 standard, -60 tight, -20 manual cut
2. TP scaling: TP1=15-30p, TP2=30-80p, TP3=100-180p
3. Market condition detection (trending/mixed/choppy)
4. Direction flipping when levels break
5. Multi-day holds for swing trades
6. 1-2% risk per trade
"""

from typing import List, Dict, Optional, Any
from dataclasses import dataclass, field


@dataclass
class FelixStrategy:
    """
    Replicates Felix VIP trading approach.
    This is a class-based strategy that can be instantiated.
    """
    name: str = "Felix Original Strategy"
    description: str = "Dynamic SL, TP scaling, and market condition detection"
    rules: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        """Initialize Felix-specific parameters."""
        self.risk_per_trade = 0.01  # 1% risk per trade
        self.default_sl_pips = 80
        self.tight_sl_pips = 60
        self.manual_cut_pips = 20
        
        # TP structure
        self.tp1_range = (15, 30)
        self.tp2_range = (30, 80)
        self.tp3_range = (100, 180)
        
        # Market condition multipliers
        self.market_multipliers = {
            'trending': {'tp3_rate': 0.75, 'sl_adjustment': 1.0},
            'mixed': {'tp3_rate': 0.40, 'sl_adjustment': 0.875},  # -70 SL
            'choppy': {'tp3_rate': 0.15, 'sl_adjustment': 0.75},   # -60 SL
        }
        
        # Key levels database (from analysis)
        self.key_levels = {
            'USDJPY': [
                {'level': 156.025, 'direction': 'Sell', 'confidence': 1.0, 'wins': 3, 'losses': 0},
                {'level': 154.950, 'direction': 'Buy', 'confidence': 0.8, 'wins': 1, 'losses': 0},
            ],
            'EURUSD': [
                {'level': 1.15980, 'direction': 'Buy', 'confidence': 1.0, 'wins': 2, 'losses': 0},
                {'level': 1.17215, 'direction': 'Buy', 'confidence': 0.8, 'wins': 2, 'losses': 0},
                {'level': 1.17550, 'direction': 'Sell', 'confidence': 0.6, 'wins': 1, 'losses': 0},
            ],
            'EURAUD': [
                {'level': 1.7745, 'direction': 'Sell', 'confidence': 1.0, 'wins': 6, 'losses': 0},
                {'level': 1.7747, 'direction': 'Sell', 'confidence': 1.0, 'wins': 6, 'losses': 0},
                {'level': 1.76875, 'direction': 'Buy', 'confidence': 0.2, 'wins': 0, 'losses': 1},
            ],
            'XAUUSD': [
                {'level': 4247, 'direction': 'Buy', 'confidence': 0.9, 'wins': 3, 'losses': 0},
                {'level': 4192, 'direction': 'Buy', 'confidence': 0.7, 'wins': 3, 'losses': 1},
                {'level': 4200, 'direction': 'Sell', 'confidence': 0.6, 'wins': 5, 'losses': 4},
                {'level': 4323, 'direction': 'Buy', 'confidence': 0.9, 'wins': 3, 'losses': 0},
                {'level': 4405, 'direction': 'Buy', 'confidence': 0.8, 'wins': 2, 'losses': 1},
            ],
            'AUDCAD': [
                {'level': 0.91620, 'direction': 'Buy', 'confidence': 1.0, 'wins': 1, 'losses': 0},
            ],
            'GBPNZD': [
                {'level': 2.29990, 'direction': 'Buy', 'confidence': 1.0, 'wins': 1, 'losses': 0},
            ],
            'GBPJPY': [
                {'level': 205.840, 'direction': 'Buy', 'confidence': 0.8, 'wins': 2, 'losses': 0},
            ],
            'EURCAD': [
                {'level': 1.60765, 'direction': 'Buy', 'confidence': 0.8, 'wins': 2, 'losses': 0},
            ],
            'USDCHF': [
                {'level': 0.80815, 'direction': 'Sell', 'confidence': 1.0, 'wins': 1, 'losses': 0},
                {'level': 0.79460, 'direction': 'Sell', 'confidence': 0.8, 'wins': 3, 'losses': 0},
            ],
        }
        
        # Flip levels (where direction reverses)
        self.flip_levels = {
            'XAUUSD': {'level': 4210, 'tolerance': 15},
            'EURUSD': {'level': 1.16500, 'tolerance': 0.0020},
            'USDJPY': {'level': 156.000, 'tolerance': 0.05},
        }
    
    def should_take_trade(self, trade) -> bool:
        """
        Determine if Felix would take this trade.
        Uses confidence scoring based on key levels and market conditions.
        """
        pair = trade.pair
        entry = trade.entry
        direction = trade.direction
        market_condition = trade.market_condition.lower() if hasattr(trade, 'market_condition') else 'unknown'
        
        if entry is None:
            return False
        
        # Get confidence score
        confidence = self._calculate_confidence(pair, entry, direction, market_condition)
        
        # Felix takes trades with confidence >= 0.6 (60%)
        return confidence >= 0.6
    
    def _calculate_confidence(self, pair: str, entry: float, direction: str, market_condition: str) -> float:
        """Calculate confidence score for a trade."""
        confidence = 0.5  # Base confidence
        
        # Check if entry is near a key level
        if pair in self.key_levels:
            for level_info in self.key_levels[pair]:
                level = level_info['level']
                tolerance = self._get_tolerance(pair, level)
                
                if abs(entry - level) <= tolerance:
                    # Entry is at a key level
                    if direction == level_info['direction']:
                        # Direction matches - boost confidence
                        win_rate = level_info['wins'] / (level_info['wins'] + level_info['losses'])
                        confidence = max(confidence, level_info['confidence'] * win_rate)
                    else:
                        # Direction doesn't match - check for flip
                        confidence = max(confidence, 0.3)  # Lower confidence for flips
        
        # Adjust for market condition
        if market_condition in self.market_multipliers:
            multiplier = self.market_multipliers[market_condition]
            confidence *= multiplier['tp3_rate'] * 1.5  # Scale by expected TP3 rate
        
        # Check flip zones
        if pair in self.flip_levels:
            flip_info = self.flip_levels[pair]
            if abs(entry - flip_info['level']) <= flip_info['tolerance']:
                # In flip zone - both directions possible
                confidence = max(confidence, 0.7)
        
        return min(confidence, 1.0)
    
    def calculate_position_size(self, account_balance: float, sl_pips: int, pair: str = "EURUSD") -> float:
        """
        Calculate position size based on 1-2% risk rule.
        
        Args:
            account_balance: Account balance in base currency
            sl_pips: Stop loss in pips
            pair: Currency pair for pip value calculation
        
        Returns:
            Position size in lots (standard = 100k units)
        """
        risk_amount = account_balance * self.risk_per_trade
        pip_value = self._get_pip_value(pair)
        
        # Position size = Risk Amount / (SL pips * Pip Value)
        position_size = risk_amount / (sl_pips * pip_value)
        
        return round(position_size, 2)
    
    def _get_pip_value(self, pair: str) -> float:
        """Get approximate pip value in USD for 1 standard lot."""
        pip_values = {
            'EURUSD': 10.0,
            'GBPUSD': 10.0,
            'USDJPY': 6.5,
            'USDCHF': 11.0,
            'AUDUSD': 10.0,
            'USDCAD': 7.5,
            'NZDUSD': 10.0,
            'XAUUSD': 10.0,  # Gold
            'EURJPY': 6.5,
            'GBPJPY': 6.5,
            'EURGBP': 13.0,
            'EURAUD': 6.5,
            'AUDCAD': 7.5,
            'AUDJPY': 6.5,
            'GBPCAD': 7.5,
            'GBPAUD': 6.5,
            'GBPNZD': 6.5,
            'EURCAD': 7.5,
            'EURCHF': 11.0,
            'CADJPY': 6.5,
            'CHFJPY': 6.5,
            'CADCHF': 11.0,
        }
        return pip_values.get(pair, 10.0)
    
    def _get_tolerance(self, pair: str, level: float) -> float:
        """Calculate entry tolerance based on pair."""
        if pair == 'XAUUSD':
            return 5.0  # 5 pips for gold
        elif 'JPY' in pair:
            return 0.05  # 5 pips for JPY pairs
        else:
            return 0.0005  # 5 pips for standard pairs
    
    def get_sl_for_market_condition(self, market_condition: str, pair: str = "EURUSD") -> int:
        """Get appropriate SL size based on market condition."""
        base_sl = self.default_sl_pips
        
        if market_condition == 'choppy':
            return int(base_sl * 0.75)  # -60 pips
        elif market_condition == 'mixed':
            return int(base_sl * 0.875)  # -70 pips
        else:
            return base_sl  # -80 pips
    
    def get_tp_targets(self, market_condition: str) -> Dict[str, int]:
        """Get TP targets based on market condition."""
        if market_condition == 'trending':
            return {
                'tp1': 30,
                'tp2': 80,
                'tp3': 180
            }
        elif market_condition == 'mixed':
            return {
                'tp1': 20,
                'tp2': 50,
                'tp3': 100
            }
        else:  # choppy
            return {
                'tp1': 15,
                'tp2': 30,
                'tp3': 60  # Rarely hit in choppy
            }
    
    def should_hold_for_tp3(self, market_condition: str, current_pips: float) -> bool:
        """
        Determine if should hold position for TP3.
        Felix only holds for TP3 in trending markets.
        """
        if market_condition == 'trending':
            return current_pips >= 50  # Hold if already +50 pips
        elif market_condition == 'mixed':
            return current_pips >= 70  # Only if strong momentum
        else:
            return False  # Don't hold for TP3 in choppy markets
    
    def should_flip_direction(self, pair: str, entry: float, direction: str) -> bool:
        """
        Determine if strategy should flip direction.
        Returns True if the level has been broken against the original direction.
        """
        if pair not in self.key_levels:
            return False
        
        for level_info in self.key_levels[pair]:
            level = level_info['level']
            tolerance = self._get_tolerance(pair, level)
            
            if abs(entry - level) <= tolerance:
                # At a key level
                if direction != level_info['direction']:
                    # Trading opposite to historical direction - potential flip
                    return True
        
        return False
    
    def get_win_rate_expectation(self, market_condition: str) -> float:
        """Get expected win rate for market condition."""
        expectations = {
            'trending': 0.75,  # 75%
            'mixed': 0.40,     # 40%
            'choppy': 0.15,    # 15%
        }
        return expectations.get(market_condition, 0.50)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert strategy configuration to dictionary."""
        return {
            'name': self.name,
            'risk_per_trade': self.risk_per_trade,
            'default_sl_pips': self.default_sl_pips,
            'tp_structure': {
                'tp1': self.tp1_range,
                'tp2': self.tp2_range,
                'tp3': self.tp3_range,
            },
            'key_levels_count': sum(len(levels) for levels in self.key_levels.values()),
            'market_multipliers': self.market_multipliers,
        }


# For compatibility with strategy runner
class FelixStrategyClass:
    """Wrapper class for compatibility with the backtester."""
    
    def __init__(self, name: str, description: str = "", rules: Dict = None):
        self.name = name
        self.description = description or "Dynamic SL, TP scaling, and market condition detection"
        self.rules = rules or {}
        self.felix = FelixStrategy()
        self.trades: List = []
    
    def should_take_trade(self, trade) -> bool:
        return self.felix.should_take_trade(trade)
    
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

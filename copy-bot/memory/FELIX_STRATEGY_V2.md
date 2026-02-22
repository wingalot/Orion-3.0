# Felix VIP Strategy v2.0
## Algoritmiska Reverse Engineering

**Izveidots:** 2026-02-16  
**Pamats:** 325+ treidi, 50+ dienu analīze (Dec 1 - Feb 14)  
**Win Rate:** 77% | **Pips:** +28,506+ | **Avg/Day:** 8.6 treidi  

---

## 🎯 STRATĒĢIJAS KOPSAVILKUMS

Felix VIP stratēģija ir **institucionālu līmeņu preces/valūtu swing tirdzniecības sistēma**, kas balstās uz:

1. **Pre-calculated key levels** (atbalsta/pretošanās)
2. **Multi-timeframe tehnisko analīzi** (D1/4H virziens, 2H/1H ieeja)
3. **Adaptive risk management** (SL: -35 līdz -180 pips pēc volatilitātes)
4. **Market condition adaptāciju** (TP1/TP2/TP3 pēc trenda spēka)
5. **Disciplinētu flip mehāniku** (virziena maiņa, ja līmenis lūst)

---

## 📊 MARKET CONDITION KLASIFIKATORS

### 3 Tirgus Stāvokļi

| Stāvoklis | TP3 Rate | Vid. Pips | Pazīmes | TP Stratēģija |
|-----------|----------|-----------|---------|---------------|
| **TRENDING** | ~75% | +873 | Strong momentum, levels break & hold | TP1+TP2+TP3 |
| **MIXED** | ~40% | +483 | Accumulation, level tests | TP1+TP2 |
| **CHOPPY** | ~15% | +272 | Range-bound, false breakouts | TP1 only |

### Klasifikācijas Algoritms

```python
def classify_market(data):
    score = {'trending': 0, 'mixed': 0, 'choppy': 0}
    
    # 1. Candlestick Pattern (30% weight)
    if strong_engulfing_4h: score['trending'] += 3
    if shooting_star_d1 or evening_star_1h: score['choppy'] += 3
    if doji_or_small_body: score['choppy'] += 2
    
    # 2. Multi-Timeframe Alignment (25% weight)
    if d1_aligned_with_4h_aligned_with_1h: score['trending'] += 3
    if mixed_signals: score['mixed'] += 2
    if conflicting: score['choppy'] += 3
    
    # 3. Level Behavior (25% weight) - CRITICAL
    if level_breaks_and_holds: score['trending'] += 3
    if level_tests_multiple_times: score['mixed'] += 2
    if false_breakout: score['choppy'] += 3
    
    # 4. Recent Performance (20% weight)
    if last_3_days_tp3_rate > 0.6: score['trending'] += 2
    elif last_3_days_tp3_rate < 0.2: score['choppy'] += 2
    else: score['mixed'] += 1
    
    return max(score, key=score.get)
```

---

## 🔑 KEY LEVEL SISTĒMA

### Līmeņu Tipi

| Tips | Apraksts | Piemēri |
|------|----------|---------|
| **Institutional** | Banku/hedžfondu līmeņi | 1.7745-1.7747 EURAUD |
| **Psychological** | Round numbers | 156.000, 1.1600 |
| **Technical** | Pivot points, S/R | S1, R1, R2, R3 |
| **Historical** | Previous day/week H/L | Dec 1 high, Nov low |

### Līmeņu Kalpošanas Laiks (Lifespan)

| Pāris | Līmenis | Dienas | Kopējie Pips |
|-------|---------|--------|--------------|
| EURAUD | 1.7745-1.7747 | 6 (Dec 16-23) | +268 |
| USDJPY | 156.025 | 3 (Dec 2-4) | +195 |
| EURUSD | 1.15980 | 3 (Dec 2,3,11) | +167+ |
| EURCAD | 1.60765 | 2 (Dec 8, 11) | +126 |
| USDCHF | 0.79460 | 3 (Dec 19, 22, 23) | +80 |

### Algoritms Līmeņu Pārvaldībai

```python
class KeyLevelManager:
    def __init__(self):
        self.levels = {}  # pair -> list of levels
        
    def add_level(self, pair, price, level_type):
        """Pievieno jaunu līmeni no tehniskās analīzes"""
        self.levels[pair].append({
            'price': price,
            'type': level_type,  # 'institutional', 'psychological', 'technical'
            'hits': 0,
            'created': today(),
            'valid': True
        })
    
    def check_level(self, pair, current_price):
        """Pārbauda vai cena tuvojas līmenim (15-50 pipu zonā)"""
        for level in self.levels[pair]:
            if abs(current_price - level['price']) <= 50:  # 50 pip zone
                return level
        return None
    
    def update_level(self, pair, level, result):
        """Atjaunina līmeni pēc treida rezultāta"""
        if result == 'TP3':
            level['hits'] += 1
            if level['hits'] >= 3:  # 3x TP3 = very strong level
                level['strength'] = 'LEGENDARY'
        elif result == 'SL':
            level['valid'] = False  # Level broken
            # Create new flipped level
            self.add_level(pair, level['price'], 'flipped')
```

---

## 🎯 ENTRY/EXIT ALGORITMS

### 1. ENTRY ZONA

| Instruments | Entry Zone | Order Tips |
|-------------|------------|------------|
| **XAUUSD** | 2-8 pips | 75% market, 25% limit |
| **Forex majors** | 1-5 pips | 75% market, 25% limit |
| **Crosses** | 5-15 pips | 75% market, 25% limit |

### 2. ORDER TIPS LOĢIKA

```python
def get_order_type(current_price, entry_zone, direction):
    if direction == 'BUY':
        if current_price <= entry_zone['max']:
            return 'MARKET'  # Price at or below entry
        else:
            return 'BUY_LIMIT'  # Wait for pullback
    else:  # SELL
        if current_price >= entry_zone['min']:
            return 'MARKET'
        else:
            return 'SELL_LIMIT'
```

### 3. SL (STOP LOSS) MEHĀNIKA

| Tirgus Stāvoklis | XAUUSD SL | Forex SL | JPY SL |
|------------------|-----------|----------|--------|
| Normal | -80 pips | -35 pips | -35 pips |
| Volatile | -120 līdz -180 | -50 pips | -60 pips |
| Tight | -60 pips | -25 pips | -25 pips |

### 4. TP (TAKE PROFIT) STRUKTŪRA

#### XAUUSD TP:
| Stāvoklis | TP1 | TP2 | TP3 |
|-----------|-----|-----|-----|
| **TRENDING** | +30 | +80 | +140/+180 |
| **MIXED** | +20/+30 | +50 | +100/+120 |
| **CHOPPY** | +20/+30 | — | — |

#### Forex TP:
| Pāris | TP1 | TP2 | TP3 |
|-------|-----|-----|-----|
| EURUSD | +10-15 | +20-50 | +36-102 |
| USDJPY | +15-20 | +30-50 | +100-132 |
| GBPJPY | +15 | +30 | +70-115 |

---

## ⚖️ RISK MANAGEMENT SISTĒMA

### 1. Risk Per Trade

```
Risk = 1-2% of account balance
Position Size = Risk Amount ÷ (SL distance in pips × Pip Value)

Example ($10,000 account, 1% risk, -80 pip SL):
- Risk amount = $100
- Position size = $100 ÷ 80 pips = $1.25 per pip
- For XAUUSD: ~0.12 lots
- For EURUSD: ~0.12 lots
```

### 2. Position Sizing Formula

```python
def calculate_position_size(account_balance, risk_percent, sl_pips, pip_value):
    risk_amount = account_balance * (risk_percent / 100)
    position_size_usd = risk_amount / sl_pips
    lots = position_size_usd / pip_value
    return lots
```

### 3. Adaptive SL pēc Volatilitātes

```python
def get_adaptive_sl(pair, atr_14, market_condition):
    base_sl = {
        'XAUUSD': 80,
        'EURUSD': 35,
        'GBPUSD': 35,
        'USDJPY': 35,
        'EURAUD': 80,
        'GBPJPY': 60
    }
    
    sl = base_sl.get(pair, 50)
    
    # Adjust for volatility
    if atr_14 > 1.5 * average_atr:  # High volatility
        sl = sl * 1.5
    elif atr_14 < 0.7 * average_atr:  # Low volatility
        sl = sl * 0.75
    
    # Adjust for market condition
    if market_condition == 'CHOPPY':
        sl = sl * 1.2  # Wider SL for choppy
    
    return round(sl)
```

### 4. TP/SL Attiecība

| Rezultāts | TP | SL | R:R |
|-----------|-----|-----|-----|
| TP1 hit | +20 | -60 | 1:3 (negatīvs) |
| TP2 hit | +50 | -60 | 1:1.2 |
| TP3 hit | +120 | -60 | 1:2 |

**Atziņa:** Win rate (77%) kompensē zemāku R:R uz TP1.

---

## 🔄 ADAPTIVE DIRECTION FLIPPING

### Kad Flip?

```python
def should_flip_direction(level, last_trade_result):
    """
    Flip direction when:
    1. Level is broken with momentum
    2. Price fails to sustain breakout
    3. Market is CHOPPY
    """
    if last_trade_result == 'SL' and level['valid'] == False:
        return True
    
    if market_condition == 'CHOPPY' and last_trade_result == 'SL':
        return True  # Quick flip in choppy
    
    return False
```

### Flip Piemēri no Datiem

| Pāris | Datums | Sākuma Virziens | SL | Flip Uz | Rezultāts |
|-------|--------|-----------------|-----|---------|-----------|
| **EURAUD** | Dec 3-4 | Buy @ 1.76875 | -80 | Sell @ 1.75520 | TP1 +20 |
| **EURUSD** | Dec 12 | Buy @ 1.15980 (3x TP3) | — | Sell @ 1.17550 | TP1 |
| **USDJPY** | Dec 15 | Sell @ 156.025 (3x TP3) | — | Buy @ 154.950 | TP2 |

---

## ⏰ DIENAS CIKLS UN POWER HOURS

### Treidu Sadalījums pa Dienu

| Laiks (GMT) | Sesija | Aktivitāte | TP3 Rate | Prioritāte |
|-------------|--------|------------|----------|------------|
| **08:00-12:00** | London | Augsta | 35% | ⭐⭐⭐⭐ |
| **13:00-17:00** | NY-London overlap | Ļoti augsta | 45% | ⭐⭐⭐⭐⭐ |
| **18:00-22:00** | NY afternoon | Vidēja | 15% | ⭐⭐ |
| **22:00-08:00** | Asia/Ziema | Zema | 10% | ⭐ |

### Dienas Cikls

```
08:00 - London Open: 2-4 treidi (agrīnie, virziena noteikšana)
09:00-12:00 - Core period: 4-6 treidi (galvenā peļņa)
12:00-13:00 - Lunch break: pauze
13:00-17:00 - NY Overlap: 2-4 treidi (labākie TP3)
17:00-20:00 - Late session: 1-2 treidi (riska samazināšana)
```

---

## 📈 STATISTIKA UN PERFORMANCE

### Kopējā Statistika (52 dienas)

| Metrika | Vērtība |
|---------|---------|
| **Kopā treidi** | 325+ |
| **Kopā pips** | +28,506+ |
| **Win rate** | ~77% |
| **Vid. treidi/dienā** | 8.6 |
| **Vid. pips/dienā** | ~548 |
| **TP3 hit rate** | 40-75% (atkarīgs no stāvokļa) |

### Labākās Dienas Pattern

| Datums | Pips | Treidi | Pattern |
|--------|------|--------|---------|
| **Feb 6** | +1909 | 14 | Gold TP3 x6, 100% win |
| **Feb 9** | +1700 | 14 | Buy limits + Gold TP3 x6 |
| **Jan 20** | +1509 | 13 | Gold Buy/Sell both TP3 |
| **Jan 27** | +1303 | 11 | Trend continuation |
| **Jan 30** | +1340 | 15 | Extreme trending |

### Sliktākās Dienas Pattern

| Datums | Pips | Treidi | Iemesls |
|--------|------|--------|---------|
| **Dec 5** | +155 | 6 | Choppy, TP1 only |
| **Dec 30** | -150 | 7 | Holiday, Gold SL x2 |
| **Jan 28** | -140 | 7 | Choppy, 3 SL hits |

---

## 🐍 PYTHON IMPLEMENTĀCIJA

```python
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

class FelixVIPStrategy:
    """
    Felix VIP Strategy v2.0
    Institutional-level swing trading system
    """
    
    def __init__(self, account_balance=10000, risk_percent=1.5):
        self.balance = account_balance
        self.risk_pct = risk_percent
        self.key_levels = {}
        self.market_condition = None
        self.trade_history = []
        
    def analyze_market(self, data):
        """Dienas sākuma analīze"""
        self.market_condition = self._classify_market(data)
        self._update_key_levels(data)
        return self.market_condition
    
    def _classify_market(self, data):
        """Market condition classifier"""
        score = {'trending': 0, 'mixed': 0, 'choppy': 0}
        
        # Candlestick patterns
        if self._has_strong_engulfing(data['4h']):
            score['trending'] += 3
        if self._has_shooting_star(data['d1']):
            score['choppy'] += 3
            
        # Level behavior
        level_behavior = self._analyze_level_behavior(data)
        if level_behavior == 'break_and_hold':
            score['trending'] += 3
        elif level_behavior == 'false_breakout':
            score['choppy'] += 3
        elif level_behavior == 'test_and_hold':
            score['mixed'] += 2
            
        # Recent performance
        recent_tp3_rate = self._get_recent_tp3_rate(days=3)
        if recent_tp3_rate > 0.6:
            score['trending'] += 2
        elif recent_tp3_rate < 0.2:
            score['choppy'] += 2
        else:
            score['mixed'] += 1
            
        return max(score, key=score.get)
    
    def check_entry(self, pair, current_price):
        """Pārbauda vai ir ieejas signāls"""
        level = self._get_nearest_level(pair, current_price)
        if not level:
            return None
            
        distance = abs(current_price - level['price'])
        if distance > 50:  # Too far from level
            return None
            
        # Confirm with lower TF
        if not self._confirm_entry_signal(pair, level):
            return None
            
        return self._create_trade_setup(pair, level, current_price)
    
    def _create_trade_setup(self, pair, level, current_price):
        """Izveido treida setupu"""
        direction = 'BUY' if current_price > level['price'] else 'SELL'
        
        # Calculate SL
        sl = self._calculate_sl(pair, level['price'])
        
        # Calculate TPs based on market condition
        tp1, tp2, tp3 = self._calculate_tps(pair, level['price'], direction)
        
        # Calculate position size
        position_size = self._calculate_position_size(sl)
        
        return {
            'pair': pair,
            'direction': direction,
            'entry': current_price,
            'sl': sl,
            'tp1': tp1,
            'tp2': tp2,
            'tp3': tp3,
            'size': position_size,
            'market_condition': self.market_condition
        }
    
    def _calculate_sl(self, pair, entry):
        """Adaptive SL calculation"""
        base_sl = {'XAUUSD': 80, 'EURUSD': 35, 'GBPJPY': 60}
        sl_pips = base_sl.get(pair, 50)
        
        # Adjust for volatility
        if self._is_high_volatility(pair):
            sl_pips *= 1.5
        
        return entry - sl_pips if 'BUY' else entry + sl_pips
    
    def _calculate_tps(self, pair, entry, direction):
        """Adaptive TP calculation"""
        multiplier = 1 if direction == 'BUY' else -1
        
        if self.market_condition == 'TRENDING':
            tp1 = entry + (30 * multiplier)
            tp2 = entry + (80 * multiplier)
            tp3 = entry + (140 * multiplier)
        elif self.market_condition == 'MIXED':
            tp1 = entry + (25 * multiplier)
            tp2 = entry + (50 * multiplier)
            tp3 = entry + (100 * multiplier) if self._strong_setup() else None
        else:  # CHOPPY
            tp1 = entry + (20 * multiplier)
            tp2 = tp3 = None
            
        return tp1, tp2, tp3
    
    def _calculate_position_size(self, sl_pips):
        """Position sizing based on risk"""
        risk_amount = self.balance * (self.risk_pct / 100)
        return risk_amount / sl_pips
    
    def on_tp1_hit(self, trade):
        """TP1 sasniegts - pārvaldīt pozīciju"""
        # Move SL to BE
        trade['sl'] = trade['entry']
        
        # If CHOPPY market, close all
        if trade['market_condition'] == 'CHOPPY':
            return 'CLOSE_ALL'
            
        # Otherwise hold for TP2/TP3
        return 'HOLD'
    
    def on_sl_hit(self, trade):
        """SL sasniegts - flip direction if needed"""
        if self.market_condition == 'CHOPPY':
            # Flip direction for next trade
            flipped_direction = 'SELL' if trade['direction'] == 'BUY' else 'BUY'
            return {
                'action': 'FLIP',
                'new_direction': flipped_direction,
                'level': trade['sl']  # Use SL level as new entry
            }
        return {'action': 'ACCEPT_LOSS'}


# Usage Example
strategy = FelixVIPStrategy(account_balance=10000, risk_percent=1.5)

# Daily analysis
market_data = load_market_data()
condition = strategy.analyze_market(market_data)
print(f"Today's market condition: {condition}")

# Check for entries
for pair in ['XAUUSD', 'EURUSD', 'GBPJPY']:
    setup = strategy.check_entry(pair, get_current_price(pair))
    if setup:
        print(f"Entry signal: {setup}")
```

---

## 🎯 PRAKTISKI IETEIKUMI

### Ieejas Signāli (BEST SETUPS)

| # | Setup | Win Rate | Vid. Pips |
|---|-------|----------|-----------|
| 1 | **USDJPY 156.025 Sell** | 100% (3/3) | +195 |
| 2 | **EURAUD 1.7745 Sell** | 83% (5/6) | +268 |
| 3 | **EURUSD 1.15980 Buy** | 100% (2/2) | +167 |
| 4 | **XAUUSD trending BUY** | 75%+ | +100-180 |
| 5 | **Multi-day hold (2-4 dienas)** | 70%+ | +100-180 |

### Ko Izvairīties

| # | Scenārijs | Iemesls |
|---|-----------|---------|
| 1 | **GBPAUD** | 2/2 zaudējumi |
| 2 | **Early gold entries** | 4192.5, 4179, 4188.8 SL |
| 3 | **Choppy days TP2/TP3** | Tikai 15% hit rate |
| 4 | **Pre-news (CPI/FOMC)** | High volatility, false breaks |

### Optimal Settings

```python
FELIX_V2_CONFIG = {
    'risk_per_trade': 1.5,  # %
    'max_trades_per_day': 15,  # Hard limit
    'min_distance_to_level': 15,  # pips
    'max_distance_to_level': 50,  # pips
    'sl_multipliers': {
        'normal': 1.0,
        'volatile': 1.5,
        'tight': 0.75
    },
    'tp_strategy': {
        'TRENDING': [1, 2, 3],  # All TPs
        'MIXED': [1, 2],  # TP1 + TP2
        'CHOPPY': [1]  # TP1 only
    },
    'power_hours': ['08:00-12:00', '13:00-17:00'],
    'core_pairs': ['XAUUSD', 'EURUSD', 'GBPJPY', 'EURAUD'],
    'flip_enabled': True,
    'be_after_tp1': True
}
```

---

## 📚 Atsauces

- **Pattern Analysis:** `memory/felix-pattern-analysis.md`
- **Risk System:** `memory/felix-risk-system.md`
- **Entry/Exit Algo:** `memory/felix-entry-exit-algo.md`
- **Market Classifier:** `memory/felix-market-classifier.md`
- **Original Analysis:** `MEMORY.md`

---

**Versija:** 2.0  
**Izveidots:** 2026-02-16  
**Autors:** AI Assistant (OpenClaw Multi-Agent Analysis)  
**Status:** ✅ Gatavs implementācijai

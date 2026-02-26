"""
Configuration manager for the trading engine.
Centralizes all configuration to prevent hard-coded values throughout the system.
"""
import os
import logging
from typing import Dict, Any
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass
class FirebaseConfig:
    """Firebase configuration dataclass"""
    service_account_path: str = os.getenv("FIREBASE_SERVICE_ACCOUNT", "./firebase-creds.json")
    project_id: str = os.getenv("FIREBASE_PROJECT_ID", "trading-engine-12345")
    database_url: str = os.getenv("FIREBASE_DATABASE_URL", "")
    collection_name: str = "trading_engine_state"

@dataclass
class ExchangeConfig:
    """Exchange configuration dataclass"""
    exchange_id: str = os.getenv("EXCHANGE_ID", "binance")
    api_key: str = os.getenv("EXCHANGE_API_KEY", "")
    api_secret: str = os.getenv("EXCHANGE_API_SECRET", "")
    sandbox_mode: bool = os.getenv("SANDBOX_MODE", "True").lower() == "true"

@dataclass
class RLConfig:
    """Reinforcement Learning configuration"""
    state_size: int = 50  # Number of features in state representation
    action_size: int = 3  # Buy, Sell, Hold
    learning_rate: float = 0.001
    discount_factor: float = 0.95
    exploration_rate: float = 0.1
    memory_size: int = 10000
    batch_size: int = 32

@dataclass
class TradingConfig:
    """Trading parameters"""
    symbols: list = None
    timeframe: str = "1h"
    initial_balance: float = 10000.0
    max_position_size: float = 0.1  # 10% of portfolio per trade
    stop_loss_pct: float = 0.02  # 2% stop loss
    take_profit_pct: float = 0.05  # 5% take profit
    risk_per_trade: float = 0.01  # Risk 1% per trade
    
    def __post_init__(self):
        if self.symbols is None:
            self.symbols = ["BTC/USDT", "ETH/USDT"]

class ConfigManager:
    """Manages all configuration for the trading engine"""
    
    def __init__(self):
        self.firebase = FirebaseConfig()
        self.exchange = ExchangeConfig()
        self.rl = RLConfig()
        self.trading = TradingConfig()
        
        # Validate critical configurations
        self._validate_configs()
        
    def _validate_configs(self) -> None:
        """Validate critical configuration values"""
        if not os.path.exists(self.firebase.service_account_path):
            logging.warning(f"Firebase service account file not found: {self.firebase.service_account_path}")
            
        if not self.exchange.api_key and not self.exchange.sandbox_mode:
            logging.error("Exchange API key missing and not in sandbox mode")
            
    def get_all_configs(self) -> Dict[str, Any]:
        """Return all configurations as dictionary"""
        return {
            "firebase": self.firebase.__dict__,
            "exchange": self.exchange.__dict__,
            "rl": self.rl.__dict__,
            "trading": self.trading.__dict__
        }

# Singleton instance
config = ConfigManager()
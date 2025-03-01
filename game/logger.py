#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Logger module for Beijing Life Story game.
Handles logging game events to a file.
"""

import os
import logging
import datetime
from typing import Dict, Any, Optional

class GameLogger:
    """
    GameLogger class to handle logging game events.
    """
    
    def __init__(self, player_name: str = "Unknown"):
        """
        Initialize the logger.
        
        Args:
            player_name: Name of the player for the log file name
        """
        # Create logs directory if it doesn't exist
        os.makedirs("logs", exist_ok=True)
        
        # Generate timestamp for log file name
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = f"logs/{timestamp}_{player_name}.log"
        
        # Configure logger
        self.logger = logging.getLogger("beijing_fushengji")
        self.logger.setLevel(logging.INFO)
        
        # Create file handler
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.INFO)
        
        # Create formatter
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        
        # Add handler to logger
        self.logger.addHandler(file_handler)
        
        # Store the log file path
        self.log_file = log_file
        
        # Log game start
        self.log_event("GAME_START", {"player_name": player_name})
    
    def log_event(self, event_type: str, data: Dict[str, Any] = None) -> None:
        """
        Log a game event.
        
        Args:
            event_type: Type of event (e.g., "TRAVEL", "BUY", "SELL")
            data: Dictionary of event data
        """
        if data is None:
            data = {}
        
        # Format the log message
        message = f"{event_type}: {data}"
        
        # Log the event
        self.logger.info(message)
    
    def log_player_status(self, player) -> None:
        """
        Log the player's current status.
        
        Args:
            player: Player object
        """
        # Extract player data
        player_data = {
            "name": player.name,
            "cash": player.cash,
            "bank_savings": player.bank_savings,
            "debt": player.debt,
            "health": player.health,
            "fame": player.fame,
            "days_left": player.days_left,
            "city": player.city,
            "current_location": player.current_location,
            "inventory_used": player.inventory_used,
            "inventory_capacity": player.inventory_capacity,
            "inventory": player.inventory
        }
        
        # Log the player status
        self.log_event("PLAYER_STATUS", player_data)
    
    def log_travel(self, player, from_location: Optional[str], to_location: str) -> None:
        """
        Log a travel event.
        
        Args:
            player: Player object
            from_location: Name of the location the player is traveling from
            to_location: Name of the location the player is traveling to
        """
        travel_data = {
            "player_name": player.name,
            "from_location": from_location,
            "to_location": to_location,
            "days_left": player.days_left
        }
        
        self.log_event("TRAVEL", travel_data)
    
    def log_buy(self, player, goods_id: int, goods_name: str, quantity: int, price: int) -> None:
        """
        Log a buy event.
        
        Args:
            player: Player object
            goods_id: ID of the goods
            goods_name: Name of the goods
            quantity: Quantity of goods bought
            price: Price per unit
        """
        buy_data = {
            "player_name": player.name,
            "goods_id": goods_id,
            "goods_name": goods_name,
            "quantity": quantity,
            "price": price,
            "total_cost": price * quantity,
            "cash_after": player.cash
        }
        
        self.log_event("BUY", buy_data)
    
    def log_sell(self, player, goods_id: int, goods_name: str, quantity: int, price: int, buy_price: int) -> None:
        """
        Log a sell event.
        
        Args:
            player: Player object
            goods_id: ID of the goods
            goods_name: Name of the goods
            quantity: Quantity of goods sold
            price: Price per unit
            buy_price: Original buy price per unit
        """
        profit = (price - buy_price) * quantity
        sell_data = {
            "player_name": player.name,
            "goods_id": goods_id,
            "goods_name": goods_name,
            "quantity": quantity,
            "price": price,
            "buy_price": buy_price,
            "profit": profit,
            "total_revenue": price * quantity,
            "cash_after": player.cash
        }
        
        self.log_event("SELL", sell_data)
    
    def log_bank_transaction(self, player, transaction_type: str, amount: int) -> None:
        """
        Log a bank transaction.
        
        Args:
            player: Player object
            transaction_type: Type of transaction (e.g., "DEPOSIT", "WITHDRAW", "REPAY")
            amount: Amount of money involved
        """
        transaction_data = {
            "player_name": player.name,
            "transaction_type": transaction_type,
            "amount": amount,
            "cash_after": player.cash,
            "bank_savings_after": player.bank_savings,
            "debt_after": player.debt
        }
        
        self.log_event("BANK_TRANSACTION", transaction_data)
    
    def log_random_event(self, event_name: str, event_description: str, effects: Dict[str, Any]) -> None:
        """
        Log a random event.
        
        Args:
            event_name: Name of the event
            event_description: Description of the event
            effects: Dictionary of effects (e.g., {"health": -10, "cash": -100})
        """
        event_data = {
            "event_name": event_name,
            "event_description": event_description,
            "effects": effects
        }
        
        self.log_event("RANDOM_EVENT", event_data)
    
    def log_game_end(self, player, reason: str, final_score: int) -> None:
        """
        Log the end of the game.
        
        Args:
            player: Player object
            reason: Reason for game end (e.g., "DAYS_OVER", "HEALTH_ZERO")
            final_score: Final score
        """
        end_data = {
            "player_name": player.name,
            "reason": reason,
            "days_played": 40 - player.days_left,
            "final_cash": player.cash,
            "final_bank_savings": player.bank_savings,
            "final_debt": player.debt,
            "final_health": player.health,
            "final_fame": player.fame,
            "final_score": final_score
        }
        
        self.log_event("GAME_END", end_data)
        
        # Log the log file path
        print(f"\n游戏日志已保存到: {self.log_file}")

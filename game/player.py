#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Player module for Beijing Life Story game.
Handles player stats, inventory, and other attributes.
"""

from typing import Dict, List, Optional

class Player:
    """
    Player class representing the game player.
    Manages player stats, inventory, and other attributes.
    """
    
    def __init__(self, name: str = "小浮生"):
        """
        Initialize a new player.
        
        Args:
            name: Player's name, defaults to "小浮生"
        """
        # Basic player info
        self.name = name
        self.days_left = 40
        
        # Player stats
        self.cash = 2000  # Initial cash
        self.debt = 5000  # Initial debt
        self.bank_savings = 0  # Initial bank savings
        self.health = 100  # Initial health
        self.fame = 100  # Initial fame
        
        # Inventory
        self.inventory: Dict[int, Dict[str, any]] = {}  # Goods in inventory
        self.inventory_capacity = 100  # Max goods capacity
        self.inventory_used = 0  # Current used capacity
        
        # Location
        self.city = "BEIJING"  # Current city (BEIJING or SHANGHAI)
        self.current_location = -1  # Current location ID (-1 means not at any location)
        
        # Special flags
        self.wangba_visits = 0  # Number of internet cafe visits
        self.sound_enabled = True  # Sound enabled flag
        self.hacker_actions_enabled = False  # Hacker actions enabled flag
    
    def get_net_worth(self) -> int:
        """
        Calculate player's net worth.
        
        Returns:
            int: Player's net worth (cash + bank_savings - debt)
        """
        return self.cash + self.bank_savings - self.debt
    
    def has_inventory_space(self, amount: int = 1) -> bool:
        """
        Check if player has enough inventory space.
        
        Args:
            amount: Amount of space needed
            
        Returns:
            bool: True if player has enough space, False otherwise
        """
        return self.inventory_used + amount <= self.inventory_capacity
    
    def add_to_inventory(self, goods_id: int, name: str, quantity: int, price: int) -> bool:
        """
        Add goods to player's inventory.
        
        Args:
            goods_id: ID of the goods
            name: Name of the goods
            quantity: Quantity to add
            price: Price per unit
            
        Returns:
            bool: True if goods were added successfully, False otherwise
        """
        if not self.has_inventory_space(quantity):
            return False
        
        # If goods already in inventory, update quantity and average price
        if goods_id in self.inventory:
            old_quantity = self.inventory[goods_id]["quantity"]
            old_price = self.inventory[goods_id]["price"]
            
            # Calculate new average price
            new_price = int((old_price * old_quantity + price * quantity) / (old_quantity + quantity))
            
            # Update inventory
            self.inventory[goods_id]["quantity"] += quantity
            self.inventory[goods_id]["price"] = new_price
        else:
            # Add new goods to inventory
            self.inventory[goods_id] = {
                "name": name,
                "quantity": quantity,
                "price": price
            }
        
        # Update inventory used
        self.inventory_used += quantity
        return True
    
    def remove_from_inventory(self, goods_id: int, quantity: int) -> bool:
        """
        Remove goods from player's inventory.
        
        Args:
            goods_id: ID of the goods
            quantity: Quantity to remove
            
        Returns:
            bool: True if goods were removed successfully, False otherwise
        """
        if goods_id not in self.inventory or self.inventory[goods_id]["quantity"] < quantity:
            return False
        
        # Update inventory
        self.inventory[goods_id]["quantity"] -= quantity
        
        # If quantity is 0, remove goods from inventory
        if self.inventory[goods_id]["quantity"] == 0:
            del self.inventory[goods_id]
        
        # Update inventory used
        self.inventory_used -= quantity
        return True
    
    def switch_city(self):
        """Switch between Beijing and Shanghai."""
        if self.city == "BEIJING":
            self.city = "SHANGHAI"
        else:
            self.city = "BEIJING"
        
        # Reset current location when switching cities
        self.current_location = -1

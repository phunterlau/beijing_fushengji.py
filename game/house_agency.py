#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
House Agency module for Beijing Life Story game.
Handles increasing player's inventory capacity.
"""

from typing import Dict, List, Optional, Tuple, Any

class HouseAgency:
    """
    HouseAgency class to handle increasing player's inventory capacity.
    """
    
    def __init__(self):
        """Initialize the house agency."""
        self.upgrade_cost = 30000  # Cost to upgrade house
        self.upgrade_amount = 10  # Amount of capacity increase per upgrade
        self.max_capacity = 140  # Maximum inventory capacity
    
    def visit(self, player, ui) -> None:
        """
        Handle player's visit to the house agency.
        
        Args:
            player: Player object
            ui: UI object for user interaction
        """
        ui.clear_screen()
        ui.show_message("欢迎来到房屋中介！")
        
        if player.inventory_capacity >= self.max_capacity:
            ui.show_message("中介说：你的房子已经是最大的了，我们没有更大的房子了。")
            return
        
        if player.cash < self.upgrade_cost:
            ui.show_message(f"中介说：你没有足够的现金来升级房子。需要至少 {self.upgrade_cost} 元。")
            return
        
        # Calculate upgrade cost based on player's wealth
        actual_cost = self.upgrade_cost
        if player.cash > self.upgrade_cost * 2:
            actual_cost = player.cash // 2  # If player is rich, charge more
        
        if not ui.ask_yes_no(f"中介说：我们可以将你的存储容量从 {player.inventory_capacity} 增加到 {player.inventory_capacity + self.upgrade_amount}，费用是 {actual_cost} 元。你要升级吗?"):
            return
        
        # Apply upgrade
        player.cash -= actual_cost
        player.inventory_capacity += self.upgrade_amount
        
        ui.show_message(f"升级完成！你的存储容量现在是 {player.inventory_capacity}")

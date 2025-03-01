#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Bank module for Beijing Life Story game.
Handles banking operations.
"""

from typing import Dict, List, Optional, Tuple, Any

class Bank:
    """
    Bank class to handle banking operations.
    """
    
    def __init__(self):
        """Initialize the bank."""
        self.deposit_interest_rate = 0.01  # 1% interest on deposits
        self.debt_interest_rate = 0.10  # 10% interest on debt
    
    def update_interest(self, player) -> None:
        """
        Update interest on player's bank savings and debt.
        
        Args:
            player: Player object
        """
        # Update bank savings interest
        player.bank_savings += int(player.bank_savings * self.deposit_interest_rate)
        
        # Update debt interest
        player.debt += int(player.debt * self.debt_interest_rate)
    
    def visit(self, player, ui, logger=None) -> None:
        """
        Handle player's visit to the bank.
        
        Args:
            player: Player object
            ui: UI object for user interaction
            logger: GameLogger object for logging (optional)
        """
        ui.clear_screen()
        ui.show_message("欢迎来到银行！")
        
        while True:
            ui.clear_screen()
            print(f"现金: {player.cash}元")
            print(f"银行存款: {player.bank_savings}元")
            print(f"债务: {player.debt}元")
            print("\n银行菜单:")
            print("  1. 存款")
            print("  2. 取款")
            print("  3. 还债")
            print("  0. 离开")
            
            choice = ui.get_input("请选择: ", input_type=int, default=0, min_value=0, max_value=3)
            
            if choice == 0:
                break
            elif choice == 1:
                self._deposit(player, ui, logger)
            elif choice == 2:
                self._withdraw(player, ui, logger)
            elif choice == 3:
                self._repay_debt(player, ui, logger)
    
    def _deposit(self, player, ui, logger=None) -> None:
        """
        Handle player's deposit to the bank.
        
        Args:
            player: Player object
            ui: UI object for user interaction
            logger: GameLogger object for logging (optional)
        """
        if player.cash <= 0:
            ui.show_message("你没有现金可以存入银行。")
            return
        
        amount = ui.get_input(f"你想存入多少钱? (最多 {player.cash}): ", 
                             input_type=int, default=0, min_value=0, max_value=player.cash)
        
        if amount <= 0:
            return
        
        player.cash -= amount
        player.bank_savings += amount
        
        # Log the transaction if logger is provided
        if logger:
            logger.log_bank_transaction(player, "DEPOSIT", amount)
        
        ui.show_message(f"你存入了 {amount} 元。新的银行存款余额: {player.bank_savings} 元")
    
    def _withdraw(self, player, ui, logger=None) -> None:
        """
        Handle player's withdrawal from the bank.
        
        Args:
            player: Player object
            ui: UI object for user interaction
            logger: GameLogger object for logging (optional)
        """
        if player.bank_savings <= 0:
            ui.show_message("你的银行账户中没有存款。")
            return
        
        amount = ui.get_input(f"你想取出多少钱? (最多 {player.bank_savings}): ", 
                             input_type=int, default=0, min_value=0, max_value=player.bank_savings)
        
        if amount <= 0:
            return
        
        player.bank_savings -= amount
        player.cash += amount
        
        # Log the transaction if logger is provided
        if logger:
            logger.log_bank_transaction(player, "WITHDRAW", amount)
        
        ui.show_message(f"你取出了 {amount} 元。新的银行存款余额: {player.bank_savings} 元")
    
    def _repay_debt(self, player, ui, logger=None) -> None:
        """
        Handle player's debt repayment.
        
        Args:
            player: Player object
            ui: UI object for user interaction
            logger: GameLogger object for logging (optional)
        """
        if player.debt <= 0:
            ui.show_message("你没有债务需要偿还。")
            return
        
        if player.cash <= 0:
            ui.show_message("你没有现金可以用来偿还债务。")
            return
        
        max_repay = min(player.cash, player.debt)
        amount = ui.get_input(f"你想偿还多少债务? (最多 {max_repay}): ", 
                             input_type=int, default=0, min_value=0, max_value=max_repay)
        
        if amount <= 0:
            return
        
        player.cash -= amount
        player.debt -= amount
        
        # Log the transaction if logger is provided
        if logger:
            logger.log_bank_transaction(player, "REPAY", amount)
        
        ui.show_message(f"你偿还了 {amount} 元债务。剩余债务: {player.debt} 元")

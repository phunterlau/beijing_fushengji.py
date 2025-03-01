#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Post Office module for Beijing Life Story game.
Handles debt management.
"""

import random
from typing import Dict, List, Optional, Tuple, Any

class PostOffice:
    """
    PostOffice class to handle debt management.
    """
    
    def __init__(self):
        """Initialize the post office."""
        pass
    
    def visit(self, player, ui) -> None:
        """
        Handle player's visit to the post office.
        
        Args:
            player: Player object
            ui: UI object for user interaction
        """
        ui.clear_screen()
        ui.show_message("欢迎来到邮局！")
        
        if player.debt <= 0:
            # Player has no debt, show different messages based on wealth
            if player.cash + player.bank_savings < 1000:
                ui.show_message("局长哈哈笑道：你没钱,真是经济差!")
            elif player.cash + player.bank_savings < 100000:
                ui.show_message("局长点点头说：\"好的,我们支援你1000元。\"")
                player.cash += 1000
            elif player.cash + player.bank_savings < 10000000:
                ui.show_message("局长在电话中称呼某人:\"老板!这里有个女的要嫁给你.\"...")
            else:
                ui.show_message("局长在电话中称呼下属说：\"请他直接到市长那里\"")
            return
        
        # Player has debt, show debt repayment options
        ui.clear_screen()
        print(f"你的债务: {player.debt}元")
        print(f"你的现金: {player.cash}元")
        
        if player.cash <= 0:
            ui.show_message("局长拿着看着雪茄，笑着说：你还想还债?你还是先去赚点钱吧！")
            return
        
        # Calculate maximum repayment amount
        max_repay = min(player.cash, player.debt)
        
        # Show repayment options
        print("\n还款选项:")
        print(f"  1. 还清所有债务 ({player.debt}元)")
        print(f"  2. 还一半债务 ({player.debt // 2}元)")
        print(f"  3. 还四分之一债务 ({player.debt // 4}元)")
        print(f"  4. 自定义还款金额 (最多 {max_repay}元)")
        print("  0. 离开")
        
        choice = ui.get_input("请选择: ", input_type=int, default=0, min_value=0, max_value=4)
        
        if choice == 0:
            return
        
        # Calculate repayment amount based on choice
        if choice == 1:
            amount = player.debt
        elif choice == 2:
            amount = player.debt // 2
        elif choice == 3:
            amount = player.debt // 4
        else:  # choice == 4
            amount = ui.get_input(f"请输入还款金额 (最多 {max_repay}元): ", 
                                 input_type=int, default=0, min_value=0, max_value=max_repay)
        
        # Check if player has enough cash
        if amount > player.cash:
            ui.show_message("局长拿着看着雪茄，笑着说：你的钱不够还这么多债务！")
            return
        
        # Confirm repayment
        if not ui.ask_yes_no(f"确定要还 {amount} 元债务吗?"):
            return
        
        # Process repayment
        player.cash -= amount
        player.debt -= amount
        
        ui.show_message(f"你偿还了 {amount} 元债务。剩余债务: {player.debt} 元")
        
        # Special message if debt is fully repaid
        if player.debt <= 0:
            ui.show_message("恭喜你还清了所有债务！")

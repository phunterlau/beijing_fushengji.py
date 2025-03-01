#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hospital module for Beijing Life Story game.
Handles health management.
"""

from typing import Dict, List, Optional, Tuple, Any

class Hospital:
    """
    Hospital class to handle health management.
    """
    
    def __init__(self):
        """Initialize the hospital."""
        self.treatment_cost_per_point = 3500  # Cost per health point
    
    def visit(self, player, ui) -> None:
        """
        Handle player's visit to the hospital.
        
        Args:
            player: Player object
            ui: UI object for user interaction
        """
        ui.clear_screen()
        ui.show_message("欢迎来到医院！")
        
        if player.health >= 100:
            ui.show_message("医生说：你的健康状况很好，不需要治疗。")
            return
        
        # Calculate treatment options
        max_treatment = 100 - player.health
        max_affordable = player.cash // self.treatment_cost_per_point
        
        if max_affordable <= 0:
            ui.show_message("医生说：你的钱不够支付任何治疗费用！")
            return
        
        # Show treatment options
        ui.clear_screen()
        print(f"你的健康值: {player.health}/100")
        print(f"你的现金: {player.cash}元")
        print(f"治疗费用: {self.treatment_cost_per_point}元/点")
        print("\n治疗选项:")
        
        options = []
        for i in range(1, min(max_treatment, max_affordable) + 1):
            if i % 5 == 0 or i == min(max_treatment, max_affordable):
                cost = i * self.treatment_cost_per_point
                options.append((i, cost))
                print(f"  {len(options)}. 恢复 {i} 点健康值 - 费用: {cost}元")
        
        print("  0. 离开")
        
        choice = ui.get_input("请选择治疗方案: ", input_type=int, default=0, min_value=0, max_value=len(options))
        
        if choice == 0:
            return
        
        # Apply treatment
        health_points, cost = options[choice - 1]
        
        if not ui.ask_yes_no(f"确定要花费 {cost} 元恢复 {health_points} 点健康值吗?"):
            return
        
        player.cash -= cost
        player.health += health_points
        
        ui.show_message(f"治疗完成！你的健康值现在是 {player.health}/100")

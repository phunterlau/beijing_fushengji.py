#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Internet Cafe module for Beijing Life Story game.
Handles internet cafe activities.
"""

import random
from typing import Dict, List, Optional, Tuple, Any

class InternetCafe:
    """
    InternetCafe class to handle internet cafe activities.
    """
    
    def __init__(self):
        """Initialize the internet cafe."""
        self.entry_fee = 15  # Cost to enter the internet cafe
        self.max_visits = 3  # Maximum number of visits allowed
        
        # Tips that can be shown in the internet cafe
        self.tips = [
            "在黑市上买卖商品是赚钱的好方法，但要小心警察。",
            "健康值低于85时，你可能会被送进医院，这会花费你的钱和时间。",
            "债务会随着时间增加，尽快还清它。",
            "银行存款会产生利息，但债务的利息更高。",
            "出售某些商品会降低你的名声，名声低会影响游戏体验。",
            "随机事件可能会影响商品价格，要随时关注市场变化。",
            "你可以在房屋中介增加存储容量，但费用很高。",
            "在医院可以恢复健康，但费用也不低。",
            "切换城市可以找到不同的商品和价格。",
            "游戏结束时，你的得分是现金+银行存款-债务。",
            "有些商品比其他商品更容易赚钱，要找出哪些是最赚钱的。",
            "如果你的健康值降到0，游戏就结束了。",
            "如果你的债务太高，可能会有人来找你麻烦。",
            "开启黑客行为可能会影响你的银行存款，但风险很高。",
            "有些地点比其他地点更危险，要小心选择。"
        ]
        
        # News that can be shown in the internet cafe
        self.news = [
            "北京市政府宣布打击假冒伪劣商品，市场上的假冒商品价格可能会上涨。",
            "海关加强对走私香烟的检查，走私香烟可能会变得更加稀缺。",
            "警方破获一起盗版软件案，盗版软件价格可能会上涨。",
            "一批假酒被查获，假酒价格可能会上涨。",
            "上海小姐服务被曝光，可能会影响其价格。",
            "进口香烟关税提高，进口香烟价格可能会上涨。",
            "水货手机市场受到打击，水货手机价格可能会上涨。",
            "假冒化妆品被曝光含有有害物质，假冒化妆品价格可能会下跌。",
            "北京市政府宣布加强对网吧的管理，网吧费用可能会上涨。",
            "医疗费用上涨，医院治疗费用可能会增加。",
            "房价上涨，房屋中介费用可能会增加。",
            "银行利率调整，存款利息可能会变化。",
            "债务利率上调，债务利息可能会增加。",
            "警方加强对黑市的打击，黑市交易可能会变得更加危险。",
            "城市之间的交通管制加强，切换城市可能会变得更加困难。"
        ]
    
    def visit(self, player, ui) -> None:
        """
        Handle player's visit to the internet cafe.
        
        Args:
            player: Player object
            ui: UI object for user interaction
        """
        ui.clear_screen()
        ui.show_message("欢迎来到网吧！")
        
        if player.wangba_visits >= self.max_visits:
            ui.show_message("老板说：你今天已经来过很多次了，明天再来吧！")
            return
        
        if player.cash < self.entry_fee:
            ui.show_message(f"老板说：上网需要 {self.entry_fee} 元，你的钱不够。")
            return
        
        # Pay entry fee
        player.cash -= self.entry_fee
        player.wangba_visits += 1
        
        # Show internet cafe menu
        while True:
            ui.clear_screen()
            print("网吧菜单:")
            print("  1. 浏览游戏攻略")
            print("  2. 查看最新新闻")
            print("  3. 黑客行为")
            print("  0. 离开")
            
            choice = ui.get_input("请选择: ", input_type=int, default=0, min_value=0, max_value=3)
            
            if choice == 0:
                break
            elif choice == 1:
                self._show_tips(player, ui)
            elif choice == 2:
                self._show_news(player, ui)
            elif choice == 3:
                self._hacker_actions(player, ui)
        
        # Give small reward for visiting
        reward = random.randint(1, 10)
        player.cash += reward
        ui.show_message(f"感谢光临！老板给了你 {reward} 元小费。")
    
    def _show_tips(self, player, ui) -> None:
        """
        Show random tips to the player.
        
        Args:
            player: Player object
            ui: UI object for user interaction
        """
        ui.clear_screen()
        print("游戏攻略:")
        
        # Show 3 random tips
        shown_tips = []
        for _ in range(3):
            tip = random.choice(self.tips)
            while tip in shown_tips:
                tip = random.choice(self.tips)
            shown_tips.append(tip)
            print(f"- {tip}")
        
        input("\n按回车键继续...")
    
    def _show_news(self, player, ui) -> None:
        """
        Show random news to the player.
        
        Args:
            player: Player object
            ui: UI object for user interaction
        """
        ui.clear_screen()
        print("最新新闻:")
        
        # Show 2 random news
        shown_news = []
        for _ in range(2):
            news = random.choice(self.news)
            while news in shown_news:
                news = random.choice(self.news)
            shown_news.append(news)
            print(f"- {news}")
        
        input("\n按回车键继续...")
    
    def _hacker_actions(self, player, ui) -> None:
        """
        Handle hacker actions.
        
        Args:
            player: Player object
            ui: UI object for user interaction
        """
        ui.clear_screen()
        
        if not player.hacker_actions_enabled:
            if not ui.ask_yes_no("警告：黑客行为可能会影响你的银行存款，但也可能带来意外收获。你确定要启用黑客行为吗?"):
                return
            
            player.hacker_actions_enabled = True
            ui.show_message("黑客行为已启用。现在你的银行存款可能会受到随机影响。")
        else:
            ui.show_message("黑客行为已经启用。你的银行存款可能会受到随机影响。")

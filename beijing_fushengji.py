#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
北京浮生记 (Beijing Life Story) - Python Command Line Version
Based on the original Visual C++ 6.0 game by Guo xianghao (2000-2012)

This is a remake of the classic Chinese game where players try to make money
by trading goods in Beijing over a 40-day period.
"""

import random
import os
import sys
import time
from typing import List, Dict, Tuple, Optional, Any

# Import game modules
from game.player import Player
from game.goods import Goods, GoodsManager
from game.locations import Location, LocationManager
from game.events import EventManager
from game.ui import UI
from game.bank import Bank
from game.hospital import Hospital
from game.house_agency import HouseAgency
from game.internet_cafe import InternetCafe
from game.post_office import PostOffice
from game.high_scores import HighScores
from game.logger import GameLogger

def main():
    """Main game function that initializes and runs the game."""
    ui = UI()
    ui.show_welcome()
    
    # Show story if player wants
    if ui.ask_yes_no("查看游戏背景故事?"):
        ui.show_story()
    
    # Get player name
    player_name = ui.get_input("请输入你的名字: ", default="小浮生")
    
    # Initialize game components
    player = Player(name=player_name)
    goods_manager = GoodsManager()
    location_manager = LocationManager()
    event_manager = EventManager()
    bank = Bank()
    hospital = Hospital()
    house_agency = HouseAgency()
    internet_cafe = InternetCafe()
    post_office = PostOffice()
    high_scores = HighScores()
    
    # Initialize logger
    logger = GameLogger(player_name)
    logger.log_player_status(player)
    
    # Show available goods in the initial city
    ui.clear_screen()
    ui.show_status(player, goods_manager, location_manager)
    ui.show_message("欢迎来到北京！")
    ui.show_available_goods(goods_manager)
    
    # Main game loop
    game_running = True
    while game_running:
        ui.clear_screen()
        ui.show_status(player, goods_manager, location_manager)
        
        # Show main menu
        choice = ui.show_main_menu(player)
        
        if choice == "travel":
            location = ui.show_location_menu(location_manager, player.city, player.current_location)
            if location is not None and hasattr(location, 'id'):
                # Get previous location name for logging
                prev_location = None
                if player.current_location:
                    prev_loc = location_manager.get_location(player.current_location, player.city)
                    prev_location = prev_loc.name if prev_loc else None
                
                # Handle travel event
                player.current_location = location.id
                player.days_left -= 1
                
                # Log travel event
                logger.log_travel(player, prev_location, location.name)
                
                # Update goods prices
                goods_manager.update_prices()
                
                # Handle random events and show news reports
                news_reports = event_manager.handle_events(player, goods_manager)
                if news_reports:
                    ui.clear_screen()
                    ui.show_status(player, goods_manager, location_manager)
                    ui.show_news_reports(news_reports)
                    
                    # Log random events
                    for report in news_reports:
                        logger.log_random_event("Random Event", report, {})
                
                # Update bank interest and debt
                bank.update_interest(player)
                
                # Update game status
                ui.show_message(f"你来到了{location.name}")
                
                # Show available goods at this location
                ui.show_available_goods(goods_manager)
                
                # Log player status after travel
                logger.log_player_status(player)
                
        elif choice == "buy":
            while True:
                result = goods_manager.buy_goods(player, ui, logger)
                if result == "exit":
                    break
            
        elif choice == "sell":
            while True:
                result = goods_manager.sell_goods(player, ui, logger)
                if result == "exit":
                    break
            
        elif choice == "bank":
            bank.visit(player, ui, logger)
            
        elif choice == "hospital":
            hospital.visit(player, ui)
            
        elif choice == "post_office":
            post_office.visit(player, ui)
            
        elif choice == "house_agency":
            house_agency.visit(player, ui)
            
        elif choice == "internet_cafe":
            internet_cafe.visit(player, ui)
            
        elif choice == "high_scores":
            high_scores.show(ui)
            
        elif choice == "switch_city":
            location_manager.switch_city(player, ui)
            
        elif choice == "help":
            ui.show_help()
            
        elif choice == "quit":
            if ui.ask_yes_no("确定要退出游戏吗?"):
                game_running = False
        
        # Check if game should end
        if player.days_left <= 0:
            ui.show_message("你在北京已经待了40天，该回家了。")
            # Sell all remaining goods
            goods_manager.sell_all_goods(player, ui, logger)
            # Calculate final score
            final_score = player.cash + player.bank_savings - player.debt
            ui.show_message(f"你的最终得分是: {final_score}")
            # Check if it's a high score
            high_scores.add_score(player.name, final_score, player.health, player.fame)
            high_scores.show(ui)
            # Log game end
            logger.log_game_end(player, "DAYS_OVER", final_score)
            game_running = False
        
        # Check if player is dead
        if player.health <= 0:
            ui.show_message("你的健康值降到了0，游戏结束!")
            # Calculate final score
            final_score = player.cash + player.bank_savings - player.debt
            # Log game end
            logger.log_game_end(player, "HEALTH_ZERO", final_score)
            game_running = False
    
    ui.show_message("谢谢游玩北京浮生记!")

if __name__ == "__main__":
    main()

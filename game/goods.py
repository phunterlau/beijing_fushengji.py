#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Goods module for Beijing Life Story game.
Handles goods and trading system.
"""

import random
from typing import Dict, List, Optional, Tuple
import questionary
from colorama import Fore, Style

class Goods:
    """
    Goods class representing a type of goods in the game.
    """
    
    def __init__(self, goods_id: int, name: str, base_price: int, price_range: int):
        """
        Initialize a new goods type.
        
        Args:
            goods_id: Unique ID for the goods
            name: Name of the goods
            base_price: Base price of the goods
            price_range: Range of price fluctuation
        """
        self.id = goods_id
        self.name = name
        self.base_price = base_price
        self.price_range = price_range
        self.current_price = 0
        self.update_price()
    
    def update_price(self) -> int:
        """
        Update the price of the goods randomly within the price range.
        
        Returns:
            int: New price of the goods
        """
        self.current_price = self.base_price + random.randint(0, self.price_range)
        return self.current_price
    
    def multiply_price(self, factor: int) -> int:
        """
        Multiply the price of the goods by a factor.
        Used for events that affect goods prices.
        
        Args:
            factor: Multiplication factor
            
        Returns:
            int: New price of the goods
        """
        self.current_price *= factor
        return self.current_price
    
    def divide_price(self, factor: int) -> int:
        """
        Divide the price of the goods by a factor.
        Used for events that affect goods prices.
        
        Args:
            factor: Division factor
            
        Returns:
            int: New price of the goods
        """
        self.current_price //= factor
        return self.current_price


class GoodsManager:
    """
    GoodsManager class to manage all goods and trading operations.
    """
    
    def __init__(self):
        """Initialize the goods manager with all available goods types."""
        # Initialize all goods types
        self.goods_types: Dict[int, Goods] = {
            0: Goods(0, "盗版软件", 100, 350),
            1: Goods(1, "走私香烟", 15000, 15000),
            2: Goods(2, "盗版VCD和游戏", 5, 50),
            3: Goods(3, "白酒（假冒伪劣）", 1000, 2500),
            4: Goods(4, "上海小姐服务（按摩服务）", 5000, 9000),
            5: Goods(5, "进口香烟", 250, 600),
            6: Goods(6, "水货手机", 750, 750),
            7: Goods(7, "假冒化妆品", 65, 180)
        }
        
        # Available goods in the market (some goods may not be available)
        self.available_goods: Dict[int, bool] = {goods_id: True for goods_id in self.goods_types}
    
    def update_prices(self, leave_out: int = 3) -> None:
        """
        Update prices of all goods and randomly make some unavailable.
        
        Args:
            leave_out: Number of goods types to leave out of the market
        """
        # Make all goods available first
        self.available_goods = {goods_id: True for goods_id in self.goods_types}
        
        # Update prices
        for goods in self.goods_types.values():
            goods.update_price()
        
        # Randomly make some goods unavailable
        for _ in range(leave_out):
            goods_id = random.choice(list(self.goods_types.keys()))
            self.available_goods[goods_id] = False
    
    def get_available_goods(self) -> List[Tuple[int, str, int]]:
        """
        Get list of available goods in the market.
        
        Returns:
            List of tuples (goods_id, name, price) for available goods
        """
        available = []
        for goods_id, available_flag in self.available_goods.items():
            if available_flag:
                goods = self.goods_types[goods_id]
                available.append((goods_id, goods.name, goods.current_price))
        return available
    
    def buy_goods(self, player, ui, logger=None) -> str:
        """
        Handle buying goods from the market.
        
        Args:
            player: Player object
            ui: UI object for user interaction
            logger: GameLogger object for logging (optional)
        """
        # Get available goods
        available_goods = self.get_available_goods()
        
        if not available_goods:
            ui.show_message("黑市上现在没有任何商品。")
            return "exit"
        
        # Create choices for the goods menu
        choices = []
        for i, (goods_id, name, price) in enumerate(available_goods, 1):
            choices.append(questionary.Choice(
                title=f"{name} - 价格: {price}",
                value=(goods_id, name, price)
            ))
        
        # Add cancel option
        choices.append(questionary.Separator())
        choices.append(questionary.Choice(title='取消', value=None))
        
        # Ask player which goods to buy
        goods_choice = ui.custom_select(
            '黑市上可用的商品:',
            choices=choices,
            parent_menu_result=None
        )
        
        if not goods_choice:
            return "exit"
        
        try:
            goods_id, name, price = goods_choice
        except (ValueError, TypeError):
            # Handle case where goods_choice is not a tuple of 3 values
            return "exit"
        
        # Check if player has enough money
        if player.cash < price:
            ui.show_message("你的现金不够买一个这样的商品。")
            return "continue"
        
        # Calculate max amount player can buy
        max_buy = min(player.cash // price, player.inventory_capacity - player.inventory_used)
        if max_buy <= 0:
            ui.show_message("你没有足够的空间或现金来购买这个商品。")
            return "continue"
        
        # Ask how many to buy
        amount = ui.get_input(f"你想买多少个 {name}? (最多 {max_buy}): ", 
                             input_type=int, default=1, min_value=1, max_value=max_buy)
        
        # Confirm purchase
        if not ui.ask_yes_no(f"确定要花费 {price * amount} 元购买 {amount} 个 {name}?"):
            return "continue"
        
        # Process purchase
        player.cash -= price * amount
        player.add_to_inventory(goods_id, name, amount, price)
        
        # Log the purchase if logger is provided
        if logger:
            logger.log_buy(player, goods_id, name, amount, price)
        
        ui.show_message(f"你购买了 {amount} 个 {name}，花费了 {price * amount} 元。")
        ui.clear_screen()
        return "continue"
    
    def sell_goods(self, player, ui, logger=None) -> str:
        """
        Handle selling goods to the market.
        
        Args:
            player: Player object
            ui: UI object for user interaction
            logger: GameLogger object for logging (optional)
        """
        if not player.inventory:
            ui.show_message("你没有任何商品可以出售。")
            return "exit"
        
        # Create choices for the inventory menu
        choices = []
        inventory_list = []
        
        for i, (goods_id, goods_info) in enumerate(player.inventory.items(), 1):
            inventory_list.append((goods_id, goods_info["name"], goods_info["quantity"], goods_info["price"]))
            
            # Check if goods is available in market
            market_price = 0
            for market_goods_id, _, price in self.get_available_goods():
                if market_goods_id == goods_id:
                    market_price = price
                    break
            
            # Prepare information for display
            is_available = market_price > 0
            is_profitable = market_price > goods_info['price']
            
            # Create title without color codes for questionary
            title = f"{goods_info['name']} - 数量: {goods_info['quantity']} - 购买价: {goods_info['price']}"
            if is_available:
                title += f" - 市场价: {market_price}"
                profit = market_price - goods_info['price']
                if profit > 0:
                    title += f" (+{profit})"
                else:
                    title += f" ({profit})"
                
            # Print colored version to console for reference
            status_line = ""
            if is_available:
                status_line += f"{Fore.GREEN}{goods_info['name']}{Style.RESET_ALL} - 数量: {goods_info['quantity']} - "
                if is_profitable:
                    status_line += f"{Fore.YELLOW}购买价: {goods_info['price']}{Style.RESET_ALL}"
                else:
                    status_line += f"{Fore.RED}购买价: {goods_info['price']}{Style.RESET_ALL}"
                
                status_line += f" - 市场价: {market_price}"
                if is_profitable:
                    status_line += f" ({Fore.GREEN}+{market_price - goods_info['price']}{Style.RESET_ALL})"
                else:
                    status_line += f" ({Fore.RED}{market_price - goods_info['price']}{Style.RESET_ALL})"
            else:
                status_line += f"{goods_info['name']} - 数量: {goods_info['quantity']} - 购买价: {goods_info['price']}"
                status_line += " (当前市场不可售)"
            
            print(f"{i}. {status_line}")
            
            choices.append(questionary.Choice(
                title=title,
                value=(goods_id, goods_info["name"], goods_info["quantity"], goods_info["price"])
            ))
        
        # Add cancel option
        choices.append(questionary.Separator())
        choices.append(questionary.Choice(title='取消', value=None))
        
        # Ask player which goods to sell
        goods_choice = ui.custom_select(
            '你的库存:',
            choices=choices,
            parent_menu_result=None
        )
        
        if not goods_choice:
            return "exit"
        
        try:
            goods_id, name, quantity, buy_price = goods_choice
        except (ValueError, TypeError):
            # Handle case where goods_choice is not a tuple of 4 values
            return "exit"
        
        # Check if the goods is available in the market
        market_price = 0
        is_available = False
        for market_goods_id, market_name, price in self.get_available_goods():
            if market_goods_id == goods_id:
                market_price = price
                is_available = True
                break
        
        if not is_available:
            ui.show_message(f"黑市上现在没有人收购 {name}。")
            return "continue"
        
        # Ask how many to sell
        amount = ui.get_input(f"你想卖多少个 {name}? (最多 {quantity}): ", 
                             input_type=int, default=1, min_value=1, max_value=quantity)
        
        # Confirm sale
        profit = (market_price - buy_price) * amount
        profit_str = f"盈利 {profit}" if profit >= 0 else f"亏损 {-profit}"
        
        if not ui.ask_yes_no(f"确定要以 {market_price} 元/个的价格出售 {amount} 个 {name}? {profit_str}"):
            return "continue"
        
        # Process sale
        player.cash += market_price * amount
        player.remove_from_inventory(goods_id, amount)
        
        # Log the sale if logger is provided
        if logger:
            logger.log_sell(player, goods_id, name, amount, market_price, buy_price)
        
        ui.show_message(f"你出售了 {amount} 个 {name}，获得了 {market_price * amount} 元。")
        ui.clear_screen()
        
        # Handle fame decrease for certain goods
        if goods_id == 4:  # 上海小姐服务
            player.fame -= 7 * amount
            if player.fame < 0:
                player.fame = 0
            ui.show_message("出售这种商品降低了你的名声！")
            ui.clear_screen()
        elif goods_id == 3:  # 白酒（假冒伪劣）
            player.fame -= 10 * amount
            if player.fame < 0:
                player.fame = 0
            ui.show_message("出售这种商品严重降低了你的名声！")
            ui.clear_screen()
        
        return "continue"
    
    def sell_all_goods(self, player, ui, logger=None) -> None:
        """
        Sell all goods in player's inventory at the end of the game.
        
        Args:
            player: Player object
            ui: UI object for user interaction
            logger: GameLogger object for logging (optional)
        """
        if not player.inventory:
            return
        
        ui.show_message("游戏结束，系统自动出售你剩余的商品:")
        
        total_earned = 0
        for goods_id, goods_info in list(player.inventory.items()):
            name = goods_info["name"]
            quantity = goods_info["quantity"]
            
            # Find market price
            market_price = 0
            is_available = False
            for market_goods_id, market_name, price in self.get_available_goods():
                if market_goods_id == goods_id:
                    market_price = price
                    is_available = True
                    break
            
            # If not available in market, use buy price
            if not is_available:
                market_price = goods_info["price"]
                ui.show_message(f"{name} 在黑市上没有人收购，以原价出售。")
            
            # Sell goods
            earned = market_price * quantity
            total_earned += earned
            
            # Log the sale if logger is provided
            if logger:
                logger.log_sell(player, goods_id, name, quantity, market_price, goods_info["price"])
            
            ui.show_message(f"出售 {quantity} 个 {name}，获得 {earned} 元")
            player.remove_from_inventory(goods_id, quantity)
        
        player.cash += total_earned
        ui.show_message(f"总共获得 {total_earned} 元")

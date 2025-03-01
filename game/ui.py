#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UI module for Beijing Life Story game.
Handles the command-line interface for the game.
"""

import os
import sys
import time
from typing import Dict, List, Optional, Tuple, Any, Union, Callable
import questionary
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

class UI:
    """
    UI class to handle the command-line interface for the game.
    """
    
    def __init__(self):
        """Initialize the UI."""
        # Define styles for questionary (can be customized)
        self.style = questionary.Style([
            ('question', 'bold'),
            ('answer', ''), # Hide the answer text
            ('pointer', 'fg:cyan bold'),
            ('highlighted', 'fg:cyan bold'),
            ('selected', 'fg:cyan bold'),
        ])
        
        # Store the current menu level for navigation
        self.menu_level = 0
        # Store the parent menu result for back navigation
        self.parent_menu_result = None
    
    def display_width(self, s):
        """
        Calculate display width of a string (Chinese characters count as 2).
        
        Args:
            s: String to calculate width for
            
        Returns:
            int: Display width of the string
        """
        width = 0
        # Remove ANSI color codes for width calculation
        clean_s = s.replace(f"{Fore.GREEN}", "").replace(f"{Fore.YELLOW}", "").replace(f"{Fore.RED}", "").replace(f"{Style.RESET_ALL}", "")
        for char in clean_s:
            if '\u4e00' <= char <= '\u9fff' or '\u3000' <= char <= '\u303f' or '\uff00' <= char <= '\uffef':  # Chinese character ranges
                width += 2
            else:
                width += 1
        return width
    
    def clear_screen(self) -> None:
        """Clear the terminal screen."""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def show_welcome(self) -> None:
        """Show the welcome message."""
        self.clear_screen()
        
        # MSDOS-style UI with box drawing characters
        print("╔" + "═" * 78 + "╗")
        print("║" + " " * 25 + "北京浮生记 (Beijing Life Story)" + " " * 25 + "║")
        print("╠" + "═" * 78 + "╣")
        print("║" + " " * 78 + "║")
        print("║ 欢迎来到北京浮生记！这是一个关于在北京生活和交易的游戏。" + " " * 20 + "║")
        print("║" + " " * 78 + "║")
        print("║ 你有40天的时间在北京各地买卖商品，赚取尽可能多的钱。" + " " * 24 + "║")
        print("║ 小心健康和名声，它们会影响你的游戏体验。" + " " * 36 + "║")
        print("║" + " " * 78 + "║")
        print("║ 祝你好运！" + " " * 68 + "║")
        print("║" + " " * 78 + "║")
        print("╚" + "═" * 78 + "╝")
        input("\n按回车键继续...")
    
    def show_story(self) -> None:
        """Show the game story."""
        self.clear_screen()
        
        # MSDOS-style UI with box drawing characters
        print("╔" + "═" * 78 + "╗")
        print("║" + " " * 34 + "游戏背景" + " " * 34 + "║")
        print("╠" + "═" * 78 + "╣")
        print("║" + " " * 78 + "║")
        print("║ 你是一个刚到北京的年轻人，只有2000元现金和5000元债务。" + " " * 24 + "║")
        print("║ 你决定通过买卖各种商品来赚钱，希望在40天内还清债务并赚取尽可能多的钱。" + " " * 8 + "║")
        print("║ 你将在北京的各个地点之间旅行，寻找最佳的交易机会。" + " " * 28 + "║")
        print("║ 但要小心，城市生活充满了危险和意外事件，可能会影响你的健康和财富。" + " " * 14 + "║")
        print("║" + " " * 78 + "║")
        print("║ 你能在这个城市中生存并成功吗？" + " " * 48 + "║")
        print("║" + " " * 78 + "║")
        print("╚" + "═" * 78 + "╝")
        input("\n按回车键继续...")
    
    def show_help(self) -> None:
        """Show the help information."""
        self.clear_screen()
        
        # MSDOS-style UI with box drawing characters
        print("╔" + "═" * 78 + "╗")
        print("║" + " " * 34 + "游戏帮助" + " " * 34 + "║")
        print("╠" + "═" * 78 + "╣")
        print("║" + " " * 78 + "║")
        print("║ 游戏目标:" + " " * 69 + "║")
        print("║   在40天内赚取尽可能多的钱，同时保持健康和名声。" + " " * 34 + "║")
        print("║" + " " * 78 + "║")
        print("║ 游戏机制:" + " " * 69 + "║")
        print("║   1. 每次移动到新位置消耗一天时间" + " " * 49 + "║")
        print("║   2. 你可以在黑市上买卖商品" + " " * 55 + "║")
        print("║   3. 商品价格会随机波动" + " " * 59 + "║")
        print("║   4. 随机事件可能会影响你的健康、名声和财富" + " " * 41 + "║")
        print("║   5. 你可以在银行存取钱和还债" + " " * 53 + "║")
        print("║   6. 你可以在医院恢复健康" + " " * 55 + "║")
        print("║   7. 你可以在房屋中介增加存储容量" + " " * 49 + "║")
        print("║   8. 你可以在网吧获取信息和小额现金" + " " * 47 + "║")
        print("║   9. 你可以在邮局还债" + " " * 59 + "║")
        print("║" + " " * 78 + "║")
        print("║ 游戏结束条件:" + " " * 65 + "║")
        print("║   1. 40天结束" + " " * 65 + "║")
        print("║   2. 健康值降到0" + " " * 63 + "║")
        print("║" + " " * 78 + "║")
        print("║ 祝你好运！" + " " * 68 + "║")
        print("║" + " " * 78 + "║")
        print("╚" + "═" * 78 + "╝")
        input("\n按回车键继续...")
    
    def show_status(self, player, goods_manager, location_manager=None) -> None:
        """
        Show the player's status.
        
        Args:
            player: Player object
            goods_manager: GoodsManager object
            location_manager: LocationManager object (optional)
        """
        # Get current location name if location_manager is provided
        current_location = ""
        if location_manager and player.current_location:
            location = location_manager.get_location(player.current_location, player.city)
            if location:
                current_location = f"   当前位置: {location.name}"
        
        
        # MSDOS-style UI with box drawing characters
        print("╔" + "═" * 78 + "╗")
        
        # Status line 1
        status1 = f"║ 玩家: {player.name}   剩余天数: {player.days_left}/40   城市: {'北京' if player.city == 'BEIJING' else '上海'}{current_location}"
        padding1 = 78 - self.display_width(status1)
        print(status1 + " " * padding1 + "║")
        
        # Status line 2
        status2 = f"║ 现金: {player.cash}元   银行存款: {player.bank_savings}元   债务: {player.debt}元"
        padding2 = 78 - self.display_width(status2)
        print(status2 + " " * padding2 + "║")
        
        # Status line 3
        status3 = f"║ 健康: {player.health}/100   名声: {player.fame}/100   库存: {player.inventory_used}/{player.inventory_capacity}"
        padding3 = 78 - self.display_width(status3)
        print(status3 + " " * padding3 + "║")
        
        if player.inventory:
            print("║" + " " * 78 + "║")
            print("║ 库存商品:" + " " * 68 + "║")
            for goods_id, goods_info in player.inventory.items():
                # Check if goods is available in market
                market_price = 0
                for market_goods_id, _, price in goods_manager.get_available_goods():
                    if market_goods_id == goods_id:
                        market_price = price
                        break
                
                # Color goods name based on availability
                if market_price > 0:
                    goods_name = f"{Fore.GREEN}{goods_info['name']}{Style.RESET_ALL}"
                else:
                    goods_name = goods_info['name']
                
                # Color price based on profitability
                if market_price > goods_info['price']:
                    price_str = f"{Fore.YELLOW}购买价: {goods_info['price']}{Style.RESET_ALL}"
                elif market_price > 0:
                    price_str = f"{Fore.RED}购买价: {goods_info['price']}{Style.RESET_ALL}"
                else:
                    price_str = f"购买价: {goods_info['price']}"
                
                # Calculate padding for right alignment
                item_text = f"  {goods_name} - 数量: {goods_info['quantity']} - {price_str}"
                padding = 78 - self.display_width(item_text)
                
                print(f"║ {item_text}" + " " * padding + "║")
        
        print("╚" + "═" * 78 + "╝")
    
    def show_available_goods(self, goods_manager) -> None:
        """
        Show available goods at the current location.
        
        Args:
            goods_manager: GoodsManager object
        """
        available_goods = goods_manager.get_available_goods()
        
        # MSDOS-style UI with box drawing characters
        print("\n╔" + "═" * 78 + "╗")
        print("║ 当前位置可用商品:" + " " * 61 + "║")
        print("╠" + "═" * 78 + "╣")
        
        if not available_goods:
            print("║ 当前位置没有可用商品。" + " " * 57 + "║")
        else:
            for i, (goods_id, name, price) in enumerate(available_goods, 1):
                item_text = f" {i}. {name} - 价格: {price}"
                padding = 78 - self.display_width(item_text)
                print(f"║{item_text}" + " " * padding + "║")
        
        print("╚" + "═" * 78 + "╝")
        input("\n按回车键继续...")
    
    def show_news_reports(self, news_reports: List[str]) -> None:
        """
        Show news reports to the player.
        
        Args:
            news_reports: List of news report messages
        """
        if not news_reports:
            return
        
        # MSDOS-style UI with box drawing characters
        print("\n╔" + "═" * 78 + "╗")
        print("║" + " " * 34 + "新闻报道" + " " * 34 + "║")
        print("╠" + "═" * 78 + "╣")
        
        for report in news_reports:
            # Split long reports into multiple lines
            words = report.split()
            lines = []
            current_line = ""
            
            for word in words:
                if len(current_line) + len(word) + 1 <= 76:  # +1 for space
                    if current_line:
                        current_line += " " + word
                    else:
                        current_line = word
                else:
                    lines.append(current_line)
                    current_line = word
            
            if current_line:
                lines.append(current_line)
            
            # Print each line with proper padding
            for line in lines:
                padding = 78 - self.display_width(line) - 2  # -2 for the "║ " prefix
                print(f"║ {line}" + " " * padding + "║")
            
            # Add a blank line between reports
            if report != news_reports[-1]:
                print("║" + " " * 78 + "║")
        
        print("╚" + "═" * 78 + "╝")
        input("\n按回车键继续...")
    
    def custom_select(self, message, choices, style=None, is_main_menu=False, parent_menu_result=None):
        """
        Custom select function with keyboard navigation.
        
        Args:
            message: The message to display
            choices: List of questionary.Choice objects
            style: The questionary style to use
            is_main_menu: Whether this is the main menu
            parent_menu_result: The result to return when left arrow is pressed
            
        Returns:
            The selected value or parent_menu_result if left arrow is pressed
        """
        import questionary
        from prompt_toolkit.formatted_text import ANSI
        
        # Set menu level
        if is_main_menu:
            self.menu_level = 0
            self.parent_menu_result = None
        
        # Create a select prompt with default settings
        # We can't easily add custom key bindings in questionary 2.1.0
        # So we'll just use the default behavior
        
        # Create a custom style that hides the answer line
        from prompt_toolkit.styles import Style as PTKStyle
        custom_style = PTKStyle.from_dict({
            'answer': 'hidden',  # Hide the answer text completely
        })
        
        select = questionary.select(
            message=message,
            choices=choices,
            style=style or self.style,
            use_indicator=False,  # Don't use the circle indicator
            use_arrow_keys=True,
            use_shortcuts=True,
            show_selected=True,
            qmark="",  # Remove the question mark
            instruction="",  # Remove the instruction text
        )
        
        # Monkey patch the select prompt to hide the answer line
        if hasattr(select, '_question') and hasattr(select._question, 'application'):
            select._question.application.style = custom_style
        
        # Run the select prompt
        result = select.ask()
        
        return result
    
    def show_main_menu(self, player) -> str:
        """
        Show the main menu and get player's choice.
        
        Args:
            player: Player object
            
        Returns:
            str: Player's choice
        """
        choices = [
            questionary.Choice(title='移动到新位置', value='travel'),
            questionary.Choice(title='购买商品', value='buy'),
            questionary.Choice(title='出售商品', value='sell'),
            questionary.Choice(title='访问银行', value='bank'),
            questionary.Choice(title='访问医院', value='hospital'),
            questionary.Choice(title='访问邮局', value='post_office'),
            questionary.Choice(title='访问房屋中介', value='house_agency'),
            questionary.Choice(title='访问网吧', value='internet_cafe'),
            questionary.Choice(title='查看高分榜', value='high_scores'),
            questionary.Choice(title='切换城市', value='switch_city'),
            questionary.Choice(title='帮助', value='help'),
            questionary.Separator(),
            questionary.Choice(title='退出游戏', value='quit')
        ]
        
        result = self.custom_select(
            "主菜单:",
            choices=choices,
            is_main_menu=True
        )
        
        return result if result else 'quit'
    
    def show_location_menu(self, location_manager, city, current_location_id=None) -> Optional[Any]:
        """
        Show the location menu and get player's choice.
        
        Args:
            location_manager: LocationManager object
            city: Current city
            current_location_id: ID of the current location (optional)
            
        Returns:
            Location object or None if cancelled
        """
        self.clear_screen()
        
        locations = location_manager.get_locations(city)
        
        # Create choices for the menu
        choices = []
        for location_id, location in locations.items():
            # If this is the current location, make it disabled
            if location_id == current_location_id:
                # For questionary, we need to use plain text without color codes
                title = f"{location.name} (当前位置)"
                choices.append(questionary.Choice(title=title, value=None, disabled="已在此位置"))
                # Print the colored version directly to console for reference
                print(f"{Fore.RED}{location.name} (当前位置){Style.RESET_ALL} - 已在此位置")
            else:
                choices.append(questionary.Choice(title=f"{location.name}", value=location))
        
        # Add return option
        choices.append(questionary.Separator())
        choices.append(questionary.Choice(title='0. 返回', value=None))
        
        # MSDOS-style UI for the menu header
        print("╔" + "═" * 78 + "╗")
        location_text = f"║ {'北京' if city == 'BEIJING' else '上海'}的位置:"
        padding = 78 - self.display_width(location_text)
        print(location_text + " " * padding + "║")
        print("╚" + "═" * 78 + "╝")
        
        # Store the parent menu result (None for returning to main menu)
        self.parent_menu_result = None
        
        result = self.custom_select(
            "",  # Empty prompt since we've already printed the header
            choices=choices,
            parent_menu_result=self.parent_menu_result
        )
        
        return result
    
    def show_message(self, message: str) -> None:
        """
        Show a message to the player.
        
        Args:
            message: Message to show
        """
        # MSDOS-style UI with box drawing characters
        print("\n╔" + "═" * 78 + "╗")
        
        # Split long messages into multiple lines
        words = message.split()
        lines = []
        current_line = ""
        
        for word in words:
            if len(current_line) + len(word) + 1 <= 76:  # +1 for space
                if current_line:
                    current_line += " " + word
                else:
                    current_line = word
            else:
                lines.append(current_line)
                current_line = word
        
        if current_line:
            lines.append(current_line)
        
        # Print each line with proper padding
        for line in lines:
            padding = 78 - self.display_width(line) - 2  # -2 for the "║ " prefix
            print(f"║ {line}" + " " * padding + "║")
        
        print("╚" + "═" * 78 + "╝")
        input("\n按回车键继续...")
    
    def get_input(self, prompt: str, input_type: Callable = str, default: Any = None, 
                 min_value: Optional[Union[int, float]] = None, 
                 max_value: Optional[Union[int, float]] = None) -> Any:
        """
        Get input from the player with validation.
        
        Args:
            prompt: Prompt to show
            input_type: Type to convert input to
            default: Default value if input is empty
            min_value: Minimum value for numeric input
            max_value: Maximum value for numeric input
            
        Returns:
            Validated input value
        """
        # For numeric input with min/max values
        if input_type in (int, float):
            # Create validation message
            validate_message = ""
            if min_value is not None and max_value is not None:
                validate_message = f" ({min_value}-{max_value})"
            elif min_value is not None:
                validate_message = f" (最小 {min_value})"
            elif max_value is not None:
                validate_message = f" (最大 {max_value})"
            
            # Define validation function
            def validate_number(text):
                if not text and default is not None:
                    return True
                
                try:
                    value = input_type(text)
                    
                    if min_value is not None and value < min_value:
                        return f"输入必须大于或等于 {min_value}"
                    
                    if max_value is not None and value > max_value:
                        return f"输入必须小于或等于 {max_value}"
                    
                    return True
                
                except ValueError:
                    return f"请输入一个有效的{input_type.__name__}"
            
            result = questionary.text(
                f"{prompt}{validate_message}",
                default=str(default) if default is not None else "",
                validate=validate_number,
                style=self.style
            ).ask()
            
            # Convert to the correct type
            if result is not None:
                try:
                    return input_type(result)
                except ValueError:
                    return default
            return default
        
        # For string or other input types
        result = questionary.text(
            prompt,
            default=default if default is not None else "",
            style=self.style
        ).ask()
        
        # Convert to the correct type if needed
        if result is not None and input_type is not str:
            try:
                return input_type(result)
            except ValueError:
                return default
        
        return result
    
    def ask_yes_no(self, prompt: str) -> bool:
        """
        Ask a yes/no question.
        
        Args:
            prompt: Question to ask
            
        Returns:
            bool: True if yes, False if no
        """
        result = questionary.confirm(
            prompt,
            default=False,
            style=self.style
        ).ask()
        
        return result if result is not None else False

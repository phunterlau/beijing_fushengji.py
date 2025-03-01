#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Locations module for Beijing Life Story game.
Handles locations in Beijing and Shanghai.
"""

from typing import Dict, List, Optional, Tuple
import questionary

class Location:
    """
    Location class representing a location in the game.
    """
    
    def __init__(self, location_id: int, name: str, city: str):
        """
        Initialize a new location.
        
        Args:
            location_id: Unique ID for the location
            name: Name of the location
            city: City the location is in (BEIJING or SHANGHAI)
        """
        self.id = location_id
        self.name = name
        self.city = city


class LocationManager:
    """
    LocationManager class to manage all locations in the game.
    """
    
    def __init__(self):
        """Initialize the location manager with all locations in Beijing and Shanghai."""
        # Initialize Beijing locations
        self.beijing_locations: Dict[int, Location] = {
            1: Location(1, "建国门", "BEIJING"),
            2: Location(2, "北京站", "BEIJING"),
            3: Location(3, "西直门", "BEIJING"),
            4: Location(4, "崇文门", "BEIJING"),
            5: Location(5, "东直门", "BEIJING"),
            6: Location(6, "复兴门", "BEIJING"),
            7: Location(7, "积水潭", "BEIJING"),
            8: Location(8, "长椿街", "BEIJING"),
            9: Location(9, "公主坟", "BEIJING"),
            10: Location(10, "苹果园", "BEIJING")
        }
        
        # Initialize Shanghai locations
        self.shanghai_locations: Dict[int, Location] = {
            1: Location(1, "人民广场", "SHANGHAI"),
            2: Location(2, "徐家汇", "SHANGHAI"),
            3: Location(3, "南京西路", "SHANGHAI"),
            4: Location(4, "淮海中路", "SHANGHAI"),
            5: Location(5, "豫园老街", "SHANGHAI"),
            6: Location(6, "外滩", "SHANGHAI"),
            7: Location(7, "陆家嘴", "SHANGHAI"),
            8: Location(8, "静安寺", "SHANGHAI"),
            9: Location(9, "徐汇路", "SHANGHAI"),
            10: Location(10, "八佰伴", "SHANGHAI")
        }
    
    def get_locations(self, city: str) -> Dict[int, Location]:
        """
        Get all locations in a city.
        
        Args:
            city: City to get locations for (BEIJING or SHANGHAI)
            
        Returns:
            Dict of location IDs to Location objects
        """
        if city == "BEIJING":
            return self.beijing_locations
        elif city == "SHANGHAI":
            return self.shanghai_locations
        else:
            return {}
    
    def get_location(self, location_id: int, city: str) -> Optional[Location]:
        """
        Get a specific location by ID and city.
        
        Args:
            location_id: ID of the location
            city: City the location is in (BEIJING or SHANGHAI)
            
        Returns:
            Location object if found, None otherwise
        """
        locations = self.get_locations(city)
        return locations.get(location_id)
    
    def get_location_name(self, location_id: int, city: str) -> str:
        """
        Get the name of a location by ID and city.
        
        Args:
            location_id: ID of the location
            city: City the location is in (BEIJING or SHANGHAI)
            
        Returns:
            Name of the location if found, empty string otherwise
        """
        location = self.get_location(location_id, city)
        return location.name if location else ""
    
    def switch_city(self, player, ui) -> None:
        """
        Handle switching cities.
        
        Args:
            player: Player object
            ui: UI object for user interaction
        """
        ui.clear_screen()
        
        # Create choices for the city menu
        choices = [
            questionary.Choice(title='1. 北京', value='BEIJING'),
            questionary.Choice(title='2. 上海', value='SHANGHAI'),
            questionary.Separator(),
            questionary.Choice(title='0. 取消', value=None)
        ]
        
        # Ask player which city to switch to
        city_choice = questionary.select(
            '选择要前往的城市:',
            choices=choices,
            style=ui.style
        ).ask()
        
        if not city_choice or city_choice == player.city:
            return
        
        # Confirm switch
        if not ui.ask_yes_no(f"确定要前往{'北京' if city_choice == 'BEIJING' else '上海'}吗? 这将消耗一天时间。"):
            return
        
        # Process switch
        player.city = city_choice
        player.current_location = 1  # Reset to first location in new city
        player.days_left -= 1
        
        ui.show_message(f"你来到了{'北京' if city_choice == 'BEIJING' else '上海'}。")

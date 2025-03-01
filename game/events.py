#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Events module for Beijing Life Story game.
Handles random events that can occur during the game.
"""

import random
from typing import Dict, List, Optional, Tuple, Any

class EventManager:
    """
    EventManager class to manage all random events in the game.
    """
    
    def __init__(self):
        """Initialize the event manager with all event types."""
        # Commercial events that affect goods prices and quantities
        self.commercial_events = []
        self._init_commercial_events()
        
        # Health events that affect player health
        self.health_events = []
        self._init_health_events()
        
        # Money events that affect player cash
        self.money_events = []
        self._init_money_events()
        
        # Locations where player can pass out
        self.pass_out_locations = [
            "建国门", "北京站", "西直门", "崇文门", "东直门",
            "复兴门", "积水潭", "长椿街", "公主坟", "苹果园",
            "人民广场", "徐家汇", "南京西路", "淮海中路", "豫园老街",
            "外滩", "陆家嘴", "静安寺", "徐汇路", "八佰伴"
        ]
        
        # Detailed locations for pass out events
        self.detailed_locations = [
            "咖啡厅", "报刊亭", "电话亭", "公共厕所亭", "公交车站口",
            "地铁站口", "女厕所门口", "中餐馆里", "电话亭里", "流浪女面前",
            "出租车上", "小商店", "电影院里", "小吃亭里", "小商场试衣间",
            "乞丐聚集地", "公共厕所亭里", "饭店里", "健身房里",
            "小巷子里", "马路边", "银行门口", "公共公园里", "医院门口",
            "公交车站里", "地铁站里", "电子游戏厅门口", "保险公司尸体门口",
            "骗子知道的地方门口"
        ]
    
    def _init_commercial_events(self):
        """Initialize commercial events."""
        self.commercial_events = [
            {
                "freq": 170,
                "msg": "专家称：进口大学生内衣在市场上供不应求，深受欢迎!",
                "goods_id": 5,  # 进口香烟
                "multiply": 2,
                "divide": 0,
                "add": 0
            },
            {
                "freq": 139,
                "msg": "卫生院检测说：市场上大量假酒，特假白酒，有毒，请勿购买!",
                "goods_id": 3,  # 白酒（假冒伪劣）
                "multiply": 3,
                "divide": 0,
                "add": 0
            },
            {
                "freq": 100,
                "msg": "医院发布重大报告：上海小姐服务效果\"非常棒\"!",
                "goods_id": 4,  # 上海小姐服务
                "multiply": 5,
                "divide": 0,
                "add": 0
            },
            {
                "freq": 41,
                "msg": "老蔡说：最近2000年诺贝尔奖获奖者，都在用盗版VCD和台片！",
                "goods_id": 2,  # 盗版VCD和游戏
                "multiply": 4,
                "divide": 0,
                "add": 0
            },
            {
                "freq": 37,
                "msg": "北京市政府：小商贩走私香烟，严重扰乱市场秩序，坚决打击!！",
                "goods_id": 1,  # 走私香烟
                "multiply": 3,
                "divide": 0,
                "add": 0
            },
            {
                "freq": 23,
                "msg": "北京市工商局：假冒化妆品，将会产生可怕到实质性的伪劣化妆品，深受欢迎!",
                "goods_id": 7,  # 假冒化妆品
                "multiply": 4,
                "divide": 0,
                "add": 0
            },
            {
                "freq": 37,
                "msg": "8858.com网站报道：上海小姐服务质量一流，请光临!",
                "goods_id": 4,  # 上海小姐服务
                "multiply": 8,
                "divide": 0,
                "add": 0
            },
            {
                "freq": 15,
                "msg": "谢霆锋代言：我用过!请使用假冒化妆品!购买假冒化妆品，永远年轻!",
                "goods_id": 7,  # 假冒化妆品
                "multiply": 7,
                "divide": 0,
                "add": 0
            },
            {
                "freq": 40,
                "msg": "北京人民开始山寨假酒，供不应求！",
                "goods_id": 3,  # 白酒（假冒伪劣）
                "multiply": 7,
                "divide": 0,
                "add": 0
            },
            {
                "freq": 29,
                "msg": "北京的大学生开始购买水货手机，深受欢迎！",
                "goods_id": 6,  # 水货手机
                "multiply": 7,
                "divide": 0,
                "add": 0
            },
            {
                "freq": 35,
                "msg": "北京的个人房改公房，走私香烟价格上涨!",
                "goods_id": 1,  # 走私香烟
                "multiply": 8,
                "divide": 0,
                "add": 0
            },
            {
                "freq": 17,
                "msg": "市场上出现大量愿意购买盗版软件!",
                "goods_id": 0,  # 盗版软件
                "multiply": 0,
                "divide": 8,
                "add": 0
            },
            {
                "freq": 24,
                "msg": "北京的孩子们都忙着上网学习，对进口香烟没有兴趣！",
                "goods_id": 5,  # 进口香烟
                "multiply": 0,
                "divide": 5,
                "add": 0
            },
            {
                "freq": 18,
                "msg": "国家严打盗版，在中关村查获一批有关盗版VCD的大案!",
                "goods_id": 2,  # 盗版VCD和游戏
                "multiply": 0,
                "divide": 8,
                "add": 0
            },
            {
                "freq": 160,
                "msg": "你的同学送给你两条走私香烟，谢谢他！",
                "goods_id": 1,  # 走私香烟
                "multiply": 0,
                "divide": 0,
                "add": 2
            },
            {
                "freq": 45,
                "msg": "警察进行扫黄打非，帮你找回了被盗丢失的盗版软件。",
                "goods_id": 0,  # 盗版软件
                "multiply": 0,
                "divide": 0,
                "add": 6
            },
            {
                "freq": 35,
                "msg": "你在回家前，一些山寨白酒（假冒伪劣）送给你!",
                "goods_id": 3,  # 白酒（假冒伪劣）
                "multiply": 0,
                "divide": 0,
                "add": 4
            },
            {
                "freq": 140,
                "msg": "媒体报道：日本生产的在中国的产品质量好! 你买了日本生产的水货手机,虽然拒绝承认长期知道信息，但是拿到了水货手机，没有任何厂商标识，硬是花了2500元。",
                "goods_id": 6,  # 水货手机
                "multiply": 0,
                "divide": 0,
                "add": 1
            }
        ]
    
    def _init_health_events(self):
        """Initialize health events."""
        self.health_events = [
            {
                "freq": 117,
                "msg": "你在街上被人敲诈勒索!",
                "damage": 3,
                "sound": "kill.wav"
            },
            {
                "freq": 157,
                "msg": "你在公交地铁上被人打了一拳! ",
                "damage": 20,
                "sound": "death.wav"
            },
            {
                "freq": 21,
                "msg": "一只疯狗追着你跑，你拼命逃跑 ",
                "damage": 1,
                "sound": "dog.wav"
            },
            {
                "freq": 100,
                "msg": "你被拥挤的交通挡在了路上! ",
                "damage": 1,
                "sound": "harley.wav"
            },
            {
                "freq": 35,
                "msg": "一小偷打了你一拳!",
                "damage": 1,
                "sound": "hit.wav"
            },
            {
                "freq": 313,
                "msg": "一群乞丐打了你!",
                "damage": 10,
                "sound": "flee.wav"
            },
            {
                "freq": 120,
                "msg": "你和同学一起小摊上挨了一砖头!",
                "damage": 5,
                "sound": "death.wav"
            },
            {
                "freq": 29,
                "msg": "你在写字楼一层被人用刀威胁!",
                "damage": 3,
                "sound": "el.wav"
            },
            {
                "freq": 43,
                "msg": "你在街上的小吃摊吃坏了! ",
                "damage": 1,
                "sound": "vomit.wav"
            },
            {
                "freq": 45,
                "msg": "你在市场上被人嘲笑，没有面子了!",
                "damage": 1,
                "sound": "level.wav"
            },
            {
                "freq": 48,
                "msg": "你被罚款40元!唉...",
                "damage": 1,
                "sound": "lan.wav"
            },
            {
                "freq": 33,
                "msg": "你在马路边看风景，被人泼了沙子!",
                "damage": 1,
                "sound": "breath.wav"
            }
        ]
    
    def _init_money_events(self):
        """Initialize money events."""
        self.money_events = [
            {
                "freq": 60,
                "msg": "你在马路上被骗子拦住，太太！",
                "ratio": 10
            },
            {
                "freq": 125,
                "msg": "一个流氓在街头拦住你，说：\"给钱！\"你：",
                "ratio": 10
            },
            {
                "freq": 100,
                "msg": "一个警察拦住你打了一下，说：\"缴费!\"你：",
                "ratio": 40
            },
            {
                "freq": 65,
                "msg": "你在马路上被一太太拦住：\"你是干什么的?交钱!\"你!",
                "ratio": 20
            },
            {
                "freq": 35,
                "msg": "电信局拦住你：\"交电话费。\"你：\"没有。\"",
                "ratio": 15
            },
            {
                "freq": 27,
                "msg": "警察说：\"你的经营证?不要去我家给我送钱哦！\"",
                "ratio": 10
            },
            {
                "freq": 40,
                "msg": "你在街上感染了疾病,要去医院治疗...",
                "ratio": 5
            }
        ]
    
    def handle_events(self, player, goods_manager) -> List[str]:
        """
        Handle all random events that can occur during the game.
        
        Args:
            player: Player object
            goods_manager: GoodsManager object
            
        Returns:
            List[str]: List of event messages to display to the player
        """
        news_reports = []
        
        # Handle commercial events
        commercial_msg = self._handle_commercial_events(player, goods_manager)
        if commercial_msg:
            news_reports.append(f"【商业新闻】{commercial_msg}")
        
        # Handle health events
        health_msg = self._handle_health_events(player)
        if health_msg:
            news_reports.append(f"【健康事件】{health_msg}")
        
        # Handle money events
        money_msg = self._handle_money_events(player)
        if money_msg:
            news_reports.append(f"【财务事件】{money_msg}")
        
        # Handle hacker events if enabled
        if player.hacker_actions_enabled:
            hacker_msg = self._handle_hacker_events(player)
            if hacker_msg:
                news_reports.append(f"【黑客事件】{hacker_msg}")
        
        return news_reports
    
    def _handle_commercial_events(self, player, goods_manager) -> None:
        """
        Handle commercial events that affect goods prices and quantities.
        
        Args:
            player: Player object
            goods_manager: GoodsManager object
        """
        for event in self.commercial_events:
            if random.randint(0, 950) % event["freq"] == 0:
                goods_id = event["goods_id"]
                
                # Skip if goods not available
                if not goods_manager.available_goods.get(goods_id, False):
                    continue
                
                # Get goods
                goods = goods_manager.goods_types[goods_id]
                
                # Apply event effects
                if event["multiply"] > 0:
                    goods.multiply_price(event["multiply"])
                
                if event["divide"] > 0:
                    goods.divide_price(event["divide"])
                
                if event["add"] > 0:
                    # Special case for the last event (adds debt)
                    if event == self.commercial_events[-1]:
                        player.debt += 2500
                    
                    # Add goods to inventory if player has space
                    add_count = min(event["add"], player.inventory_capacity - player.inventory_used)
                    if add_count > 0:
                        player.add_to_inventory(
                            goods_id,
                            goods.name,
                            add_count,
                            0  # Free goods
                        )
                
                # Return the event message
                return event["msg"]
    
    def _handle_health_events(self, player) -> None:
        """
        Handle health events that affect player health.
        
        Args:
            player: Player object
        """
        for event in self.health_events:
            if random.randint(0, 1000) % event["freq"] == 0:
                # Apply health damage
                player.health -= event["damage"]
                
                # Check if player needs medical care
                if player.health < 85 and player.days_left > 3:
                    # Player needs medical care
                    delay_days = 1 + random.randint(0, 1)
                    location_index = (10 * (1 if player.city == "BEIJING" else 0) + player.current_location - 1)
                    location = self.pass_out_locations[location_index] if 0 <= location_index < len(self.pass_out_locations) else "某地"
                    detailed_location = random.choice(self.detailed_locations)
                    
                    # Calculate medical cost
                    medical_cost = delay_days * (1000 + random.randint(0, 8500))
                    
                    # Add to debt
                    player.debt += medical_cost
                    
                    # Increase health
                    player.health += 10
                    if player.health > 100:
                        player.health = 100
                    
                    # Decrease days left
                    player.days_left -= delay_days
                    
                    # Return the event message
                    return f"你的身体不行了，送进了医院，医生说你需要休息{delay_days}天。\n" \
                           f"你在昏迷中注射了葡萄糖,我被人发现躺在{location}附近的{detailed_location}里。\n" \
                           f"医院院长为我垫付了住院费用{medical_cost}元。"
                
                # Return the event message
                return f"{event['msg']}\n你的健康值减少了{event['damage']}点。"
    
    def _handle_money_events(self, player) -> None:
        """
        Handle money events that affect player cash.
        
        Args:
            player: Player object
        """
        for event in self.money_events:
            if random.randint(0, 1000) % event["freq"] == 0:
                # Calculate money loss
                money_loss = (player.cash * event["ratio"]) // 100
                
                # Apply money loss
                player.cash -= money_loss
                if player.cash < 0:
                    player.cash = 0
                
                # Return the event message
                return f"{event['msg']}\n你的现金减少了{event['ratio']}%。"
    
    def _handle_hacker_events(self, player) -> None:
        """
        Handle hacker events that affect player's bank savings.
        
        Args:
            player: Player object
        """
        if random.randint(0, 1000) % 25 == 0:
            if player.bank_savings < 1000:
                return
            
            if player.bank_savings > 100000:
                # Large savings, can lose or gain money
                amount = player.bank_savings // (2 + random.randint(0, 19))
                
                if random.randint(0, 20) % 3 != 0:
                    # Lose money
                    player.bank_savings -= amount
                    return f"在黑客入侵银行网络，试图修改数据库，我的存款减少了{amount}"
                else:
                    # Gain money
                    player.bank_savings += amount
                    return f"在黑客入侵银行网络，试图修改数据库，我的存款增加了{amount}"
            else:
                # Smaller savings, always gain money
                amount = player.bank_savings // (1 + random.randint(0, 14))
                player.bank_savings += amount
                return f"在黑客入侵银行网络，试图修改数据库，我的存款增加了{amount}"

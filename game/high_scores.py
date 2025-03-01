#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
High Scores module for Beijing Life Story game.
Handles tracking high scores.
"""

import os
import json
from typing import Dict, List, Optional, Tuple, Any

class HighScores:
    """
    HighScores class to handle tracking high scores.
    """
    
    def __init__(self, scores_file: str = "scores.json"):
        """
        Initialize the high scores.
        
        Args:
            scores_file: Path to the scores file
        """
        self.scores_file = scores_file
        self.scores = self._load_scores()
    
    def _load_scores(self) -> List[Dict[str, Any]]:
        """
        Load high scores from file.
        
        Returns:
            List of high score entries
        """
        if os.path.exists(self.scores_file):
            try:
                with open(self.scores_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                # If file is corrupted or can't be read, return empty list
                return []
        else:
            # If file doesn't exist, return empty list
            return []
    
    def _save_scores(self) -> None:
        """Save high scores to file."""
        try:
            with open(self.scores_file, "w", encoding="utf-8") as f:
                json.dump(self.scores, f, ensure_ascii=False, indent=2)
        except IOError:
            # If file can't be written, just ignore
            pass
    
    def add_score(self, name: str, score: int, health: int, fame: int) -> bool:
        """
        Add a new high score.
        
        Args:
            name: Player's name
            score: Player's score
            health: Player's health
            fame: Player's fame
            
        Returns:
            bool: True if score was added to top 10, False otherwise
        """
        # Create new score entry
        new_score = {
            "name": name,
            "score": score,
            "health": health,
            "fame": fame
        }
        
        # Add score to list
        self.scores.append(new_score)
        
        # Sort scores by score (descending)
        self.scores.sort(key=lambda x: x["score"], reverse=True)
        
        # Keep only top 10 scores
        if len(self.scores) > 10:
            self.scores = self.scores[:10]
            # Check if new score is in top 10
            return any(s["name"] == name and s["score"] == score for s in self.scores)
        else:
            # If less than 10 scores, new score is definitely in top 10
            self._save_scores()
            return True
    
    def get_rank(self, score: int) -> int:
        """
        Get rank for a score.
        
        Args:
            score: Score to get rank for
            
        Returns:
            int: Rank (1-10) or 0 if not in top 10
        """
        for i, s in enumerate(self.scores):
            if score >= s["score"]:
                return i + 1
        
        if len(self.scores) < 10:
            return len(self.scores) + 1
        else:
            return 0
    
    def show(self, ui) -> None:
        """
        Show high scores.
        
        Args:
            ui: UI object for user interaction
        """
        ui.clear_screen()
        print("=" * 80)
        print("                                高分榜")
        print("=" * 80)
        
        if not self.scores:
            print("\n还没有高分记录。")
        else:
            print("\n排名  姓名                  得分      健康    名声")
            print("-" * 80)
            
            for i, score in enumerate(self.scores):
                print(f"{i+1:2d}.   {score['name']:<20s}  {score['score']:<8d}  {score['health']:<6d}  {score['fame']:<6d}")
        
        print("\n" + "=" * 80)
        input("\n按回车键继续...")

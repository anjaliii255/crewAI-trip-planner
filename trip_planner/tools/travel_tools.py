from langchain.tools import BaseTool
from typing import Optional, Type, Dict, Any, List
from pydantic import BaseModel, Field
import requests
import json
from datetime import datetime, timedelta

class TravelTools:
    @staticmethod
    def calculate_match_score(city: Dict[str, Any], preferences: List[str], budget: float, season: str) -> float:
        """Calculate how well a city matches the user's preferences."""
        score = 0.0
        max_score = 1.0
        
        # Preference matching (40% of total score)
        preference_weights = {
            "Beach": ["coastal", "beach", "seaside", "ocean"],
            "Mountains": ["mountain", "hiking", "skiing", "alpine"],
            "City Life": ["urban", "metropolitan", "city", "downtown"],
            "Culture": ["museum", "art", "history", "cultural", "heritage"],
            "Food": ["cuisine", "restaurant", "gastronomy", "culinary"],
            "Adventure": ["adventure", "outdoor", "sports", "activities"],
            "Relaxation": ["spa", "wellness", "peaceful", "tranquil"],
            "Nightlife": ["nightlife", "entertainment", "bars", "clubs"]
        }
        
        description = city.get("description", "").lower()
        for pref in preferences:
            if pref in preference_weights:
                for keyword in preference_weights[pref]:
                    if keyword in description:
                        score += 0.1  # 0.1 points per matching keyword
        
        # Budget matching (30% of total score)
        daily_cost = city.get("estimated_cost", {}).get("total_per_day", 0)
        if daily_cost <= budget:
            score += 0.3  # Full points if within budget
        else:
            # Reduce score based on how much over budget
            budget_diff = (daily_cost - budget) / budget
            score += max(0, 0.3 * (1 - budget_diff))
        
        # Season matching (30% of total score)
        season_weather = {
            "Spring": ["mild", "spring", "pleasant", "temperate"],
            "Summer": ["hot", "summer", "warm", "sunny"],
            "Fall": ["autumn", "fall", "cool", "mild"],
            "Winter": ["cold", "winter", "snow", "chilly"]
        }
        
        if season in season_weather:
            for keyword in season_weather[season]:
                if keyword in description:
                    score += 0.1  # 0.1 points per matching season keyword
        
        # Normalize score to be between 0 and 1
        return min(max(score, 0), 1)

    @staticmethod
    def calculate_travel_budget(destination: str, duration: int, preferences: list) -> Dict[str, float]:
        """Calculate estimated travel budget based on destination, duration, and preferences."""
        # Placeholder implementation
        return {
            "accommodation": 100 * duration,
            "food": 50 * duration,
            "activities": 75 * duration,
            "transportation": 200,
            "total": (100 + 50 + 75) * duration + 200
        }

    @staticmethod
    def get_safety_information(destination: str) -> str:
        """Get safety information for a destination."""
        # Placeholder implementation
        return json.dumps({
            "general_safety": "Generally safe for tourists",
            "health_concerns": "No major health concerns",
            "crime_rate": "Low",
            "natural_disasters": "Low risk"
        })

    @staticmethod
    def get_weather_forecast(destination: str, date: str = None) -> Dict[str, Any]:
        """Get weather forecast for a destination and date."""
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
            
        # Placeholder implementation
        return {
            "temperature": 25,
            "condition": "Sunny",
            "humidity": 60,
            "wind_speed": 10
        }

    @staticmethod
    def get_local_events(destination: str, date_range: Dict[str, str] = None) -> list:
        """Get local events for a destination within a date range."""
        if date_range is None:
            today = datetime.now()
            date_range = {
                "start": today.strftime("%Y-%m-%d"),
                "end": (today + timedelta(days=7)).strftime("%Y-%m-%d")
            }
            
        # Placeholder implementation
        return [
            {
                "name": "Local Festival",
                "date": date_range["start"],
                "description": "Annual cultural festival",
                "location": "City Center"
            }
        ] 
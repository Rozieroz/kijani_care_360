import os
import httpx
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class WeatherService:
    def __init__(self):
        self.api_key = os.getenv("OPENWEATHER_API_KEY")
        self.base_url = "https://api.openweathermap.org/data/2.5"
        self.geo_url = "https://api.openweathermap.org/geo/1.0"
        
    async def get_coordinates(self, city: str, country: str = "KE") -> Optional[Dict[str, float]]:
        """Get coordinates for a city"""
        if not self.api_key:
            return None
            
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.geo_url}/direct",
                    params={
                        "q": f"{city},{country}",
                        "limit": 1,
                        "appid": self.api_key
                    }
                )
                
                if response.status_code == 200:
                    data = response.json()
                    if data:
                        return {"lat": data[0]["lat"], "lon": data[0]["lon"]}
        except Exception as e:
            logger.error(f"Error getting coordinates: {e}")
            
        return None
    
    async def get_current_weather(self, lat: float, lon: float) -> Optional[Dict[str, Any]]:
        """Get current weather for coordinates"""
        if not self.api_key:
            return self._get_mock_current_weather()
            
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/weather",
                    params={
                        "lat": lat,
                        "lon": lon,
                        "appid": self.api_key,
                        "units": "metric"
                    }
                )
                
                if response.status_code == 200:
                    data = response.json()
                    return {
                        "temperature": round(data["main"]["temp"]),
                        "condition": data["weather"][0]["main"],
                        "description": data["weather"][0]["description"],
                        "humidity": data["main"]["humidity"],
                        "wind_speed": round(data["wind"]["speed"] * 3.6),  # Convert m/s to km/h
                        "pressure": data["main"]["pressure"],
                        "visibility": data.get("visibility", 10000) / 1000,  # Convert to km
                        "feels_like": round(data["main"]["feels_like"])
                    }
        except Exception as e:
            logger.error(f"Error getting current weather: {e}")
            
        return self._get_mock_current_weather()
    
    async def get_forecast(self, lat: float, lon: float) -> Optional[list]:
        """Get 5-day weather forecast"""
        if not self.api_key:
            return self._get_mock_forecast()
            
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/forecast",
                    params={
                        "lat": lat,
                        "lon": lon,
                        "appid": self.api_key,
                        "units": "metric"
                    }
                )
                
                if response.status_code == 200:
                    data = response.json()
                    forecast = []
                    
                    # Group by day and get daily highs/lows
                    daily_data = {}
                    for item in data["list"]:
                        date = datetime.fromtimestamp(item["dt"]).date()
                        if date not in daily_data:
                            daily_data[date] = {
                                "temps": [],
                                "conditions": [],
                                "rain_probs": []
                            }
                        
                        daily_data[date]["temps"].append(item["main"]["temp"])
                        daily_data[date]["conditions"].append(item["weather"][0]["main"])
                        daily_data[date]["rain_probs"].append(item.get("pop", 0) * 100)
                    
                    # Convert to forecast format
                    days = ["Today", "Tomorrow", "Friday", "Saturday", "Sunday"]
                    for i, (date, data_item) in enumerate(list(daily_data.items())[:5]):
                        day_name = days[i] if i < len(days) else date.strftime("%A")
                        forecast.append({
                            "day": day_name,
                            "date": date.isoformat(),
                            "high": round(max(data_item["temps"])),
                            "low": round(min(data_item["temps"])),
                            "condition": max(set(data_item["conditions"]), key=data_item["conditions"].count),
                            "rain_chance": round(max(data_item["rain_probs"]))
                        })
                    
                    return forecast
        except Exception as e:
            logger.error(f"Error getting forecast: {e}")
            
        return self._get_mock_forecast()
    
    def get_planting_advice(self, current_weather: Dict[str, Any], forecast: list) -> Dict[str, Any]:
        """Generate tree planting advice based on weather conditions"""
        temp = current_weather.get("temperature", 20)
        humidity = current_weather.get("humidity", 50)
        condition = current_weather.get("condition", "Clear").lower()
        
        # Determine if it's a good day for planting
        is_good_day = True
        recommendations = []
        
        # Temperature checks
        if temp < 10:
            is_good_day = False
            recommendations.append("Too cold for planting. Wait for warmer weather.")
        elif temp > 35:
            is_good_day = False
            recommendations.append("Too hot for planting. Consider waiting for cooler weather.")
        elif 15 <= temp <= 30:
            recommendations.append("Perfect temperature for tree planting!")
        
        # Humidity checks
        if humidity < 30:
            recommendations.append("Low humidity - ensure extra watering after planting.")
        elif humidity > 80:
            recommendations.append("High humidity - good for tree establishment.")
        
        # Weather condition checks
        if "rain" in condition or "storm" in condition:
            is_good_day = False
            recommendations.append("Avoid planting during rain or storms.")
        elif "snow" in condition:
            is_good_day = False
            recommendations.append("Snow conditions are not suitable for planting.")
        elif condition in ["clear", "sunny"]:
            recommendations.append("Clear weather is excellent for planting!")
        
        # Check upcoming rain in forecast
        upcoming_rain = any(day.get("rain_chance", 0) > 60 for day in forecast[:3])
        if upcoming_rain:
            recommendations.append("Rain expected in coming days - great for newly planted trees!")
        
        # Best time recommendations
        if temp > 25:
            best_time = "Early morning (6-8 AM) or late afternoon (5-7 PM)"
        else:
            best_time = "Mid-morning (8-10 AM) or afternoon (2-5 PM)"
        
        # Watering advice
        if humidity < 40 or temp > 28:
            watering_needed = "Heavy watering recommended due to dry/hot conditions"
        elif humidity > 70:
            watering_needed = "Light watering sufficient due to high humidity"
        else:
            watering_needed = "Moderate watering recommended"
        
        return {
            "is_good_day": is_good_day,
            "recommendation": " ".join(recommendations) if recommendations else "Good conditions for tree planting!",
            "best_time": best_time,
            "watering_needed": watering_needed,
            "temperature_rating": "optimal" if 15 <= temp <= 30 else "suboptimal",
            "humidity_rating": "good" if 40 <= humidity <= 80 else "challenging"
        }
    
    def _get_mock_current_weather(self) -> Dict[str, Any]:
        """Fallback mock weather data"""
        return {
            "temperature": 24,
            "condition": "Partly Cloudy",
            "description": "partly cloudy",
            "humidity": 65,
            "wind_speed": 12,
            "pressure": 1013,
            "visibility": 10,
            "feels_like": 26
        }
    
    def _get_mock_forecast(self) -> list:
        """Fallback mock forecast data"""
        return [
            {"day": "Today", "date": datetime.now().date().isoformat(), "high": 26, "low": 18, "condition": "Sunny", "rain_chance": 10},
            {"day": "Tomorrow", "date": (datetime.now() + timedelta(days=1)).date().isoformat(), "high": 25, "low": 17, "condition": "Cloudy", "rain_chance": 30},
            {"day": "Friday", "date": (datetime.now() + timedelta(days=2)).date().isoformat(), "high": 22, "low": 16, "condition": "Rainy", "rain_chance": 80},
            {"day": "Saturday", "date": (datetime.now() + timedelta(days=3)).date().isoformat(), "high": 24, "low": 18, "condition": "Partly Cloudy", "rain_chance": 20},
            {"day": "Sunday", "date": (datetime.now() + timedelta(days=4)).date().isoformat(), "high": 27, "low": 19, "condition": "Sunny", "rain_chance": 5}
        ]

# Global instance
weather_service = WeatherService()
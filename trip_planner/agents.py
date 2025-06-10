from crewai import Agent
from textwrap import dedent
from langchain_openai import ChatOpenAI
import os
from typing import List, Dict, Any
from pydantic import BaseModel, Field, validator
from langchain.tools import Tool
from trip_planner.tools import (
    CalculatorTools,
    SearchTools,
    TravelTools
)
from trip_planner.guardrails import GuardrailManager


class TravelInput(BaseModel):
    """Input validation for travel planning requests"""
    destination: str
    start_date: str
    end_date: str
    activities: List[str] = Field(..., min_items=1)
    accommodation: str

    @validator('activities')
    def validate_activities(cls, v):
        allowed = {"Sightseeing", "Museums", "Shopping", "Local Food", 
                  "Adventure Sports", "Relaxation", "Nightlife"}
        if not all(act in allowed for act in v):
            raise ValueError(f"Invalid activities. Allowed values: {allowed}")
        return v

    @validator('accommodation')
    def validate_accommodation(cls, v):
        allowed = {"Budget", "Mid-range", "Luxury"}
        if v not in allowed:
            raise ValueError(f"Invalid accommodation type. Allowed values: {allowed}")
        return v

    @validator('end_date')
    def validate_dates(cls, v, values):
        if 'start_date' in values:
            start = datetime.strptime(values['start_date'], "%Y-%m-%d")
            end = datetime.strptime(v, "%Y-%m-%d")
            if end < start:
                raise ValueError("End date must be after start date")
            if (end - start).days > 90:
                raise ValueError("Trip duration cannot exceed 90 days")
        return v


class TravelOutput(BaseModel):
    """Output validation for travel planning responses"""
    itinerary: List[Dict[str, Any]]
    budget_breakdown: Dict[str, float]
    recommendations: List[str]

    @validator('budget_breakdown')
    def validate_budget(cls, v):
        required = {"accommodation", "food", "activities", "transportation", "total"}
        if not all(key in v for key in required):
            raise ValueError(f"Budget breakdown must include: {required}")
        if v['total'] != sum(v[k] for k in required if k != 'total'):
            raise ValueError("Total must equal sum of all costs")
        return v


class CityInput(BaseModel):
    """Input validation for city selection requests"""
    preferences: List[str] = Field(..., min_items=1)
    budget: float = Field(..., gt=0, le=10000)
    duration: int = Field(..., gt=0, le=90)
    season: str

    @validator('preferences')
    def validate_preferences(cls, v):
        allowed = {"Beach", "Mountains", "City Life", "Culture", "Food", 
                  "Adventure", "Relaxation", "Nightlife"}
        if not all(pref in allowed for pref in v):
            raise ValueError(f"Invalid preferences. Allowed values: {allowed}")
        return v

    @validator('season')
    def validate_season(cls, v):
        allowed = {"Spring", "Summer", "Fall", "Winter"}
        if v not in allowed:
            raise ValueError(f"Invalid season. Allowed values: {allowed}")
        return v


class CityOutput(BaseModel):
    """Output validation for city selection responses"""
    recommended_cities: List[Dict[str, Any]] = Field(..., description="List of recommended cities with details")

    @validator('recommended_cities')
    def validate_cities(cls, v):
        for city in v:
            required_fields = {
                "name", "country", "description", "match_score",
                "highlights", "estimated_cost"
            }
            if not all(field in city for field in required_fields):
                raise ValueError(f"Each city must include: {required_fields}")
            
            cost_fields = {
                "accommodation", "food", "activities", "total_per_day"
            }
            if not all(field in city["estimated_cost"] for field in cost_fields):
                raise ValueError(f"Each city's estimated_cost must include: {cost_fields}")
            
            if not isinstance(city["highlights"], list):
                raise ValueError("highlights must be a list")
            
            if not isinstance(city["match_score"], (int, float)):
                raise ValueError("match_score must be a number")
            
            if not all(isinstance(cost, (int, float)) for cost in city["estimated_cost"].values()):
                raise ValueError("All cost values must be numbers")
        
        return v


class TripAgents:
    def __init__(self, llm: ChatOpenAI):
        self.llm = llm
        self.guardrails = GuardrailManager()

    def expert_travel_agent(self):
        return Agent(
            role="Expert Travel Agent",
            backstory=dedent(f"""Expert in travel planning and logistics. 
                             I have decades of experience making travel iteneraries"""),
            goal=dedent(f"""
                        Create a detailed travel itinerary based on the specified duration,
                        include budget, packing suggestions, and safety tips.
                        The itinerary should be customized to the traveler's preferences
                        and constraints while staying within the specified budget.
                        """),
            tools=[
                SearchTools.search_internet,
                CalculatorTools.calculate,
                TravelTools.calculate_travel_budget,
                TravelTools.get_safety_information,
                TravelTools.get_weather_forecast
            ],
            verbose=True,
            llm=self.llm,
            input_schema=TravelInput,
            output_schema=TravelOutput,
            input_validation=True,
            output_validation=True
        )

    def city_selection_expert(self) -> Agent:
        """Create an agent for city selection"""
        return Agent(
            role="City Selection Expert",
            goal="Recommend the best cities based on user preferences and constraints",
            backstory="""You are an expert travel advisor with extensive knowledge of cities worldwide.\nYou specialize in matching travelers with destinations that best suit their preferences,\nbudget, and travel style. Use the calculate_match_score tool to evaluate how well each city\nmatches the user's preferences.\nNEVER attempt to delegate work to a co-worker. If you cannot find real cities, return a static JSON with at least one city recommendation in the required format.\nExample fallback:\n{\n  \"recommended_cities\": [\n    {\n      \"name\": \"Barcelona\",\n      \"country\": \"Spain\",\n      \"description\": \"A vibrant city known for its beaches and rich cultural heritage.\",\n      \"match_score\": 0.9,\n      \"highlights\": [\"Sagrada Familia\", \"Beach\", \"Local Cuisine\"],\n      \"estimated_cost\": {\n        \"accommodation\": 80,\n        \"food\": 40,\n        \"activities\": 30,\n        \"total_per_day\": 150\n      }\n    }\n  ]\n}\n""",
            verbose=True,
            llm=self.llm,
            tools=[
                Tool(
                    name="search_internet",
                    func=SearchTools.search_internet,
                    description="Search the internet for information about cities and destinations"
                ),
                Tool(
                    name="calculate_travel_budget",
                    func=TravelTools.calculate_travel_budget,
                    description="Calculate estimated travel budget for a destination"
                ),
                Tool(
                    name="get_safety_information",
                    func=TravelTools.get_safety_information,
                    description="Get safety information for a destination"
                ),
                Tool(
                    name="calculate_match_score",
                    func=TravelTools.calculate_match_score,
                    description="Calculate how well a city matches the user's preferences"
                )
            ],
            input_schema=CityInput,
            output_schema=CityOutput,
            input_validation=True,
            output_validation=True,
            output_format={
                "type": "json",
                "schema": {
                    "recommended_cities": [
                        {
                            "name": "string",
                            "country": "string",
                            "description": "string",
                            "match_score": "number",
                            "highlights": ["string"],
                            "estimated_cost": {
                                "accommodation": "number",
                                "food": "number",
                                "activities": "number",
                                "total_per_day": "number"
                            }
                        }
                    ]
                }
            }
        )

    def local_tour_guide(self):
        return Agent(
            role="Local Tour Guide",
            backstory=dedent(f"""I am an experienced local tour guide who knows all the hidden gems and must-see spots in the city."""),
            goal=dedent(f"""Create a detailed itinerary for a day tour in the city, including food recommendations, cultural experiences, and shopping spots."""),
            tools=[
                SearchTools.search_internet,
                TravelTools.get_local_events,
                TravelTools.get_restaurant_recommendations
            ],
            verbose=True,
            llm=self.llm,
        )
    
    def transportation_specialist(self):
        return Agent(
            role="Transportation Specialist",
            backstory=dedent(f"""I am a transportation expert with extensive knowledge of various travel methods, routes, and transit systems worldwide. 
                             I specialize in optimizing travel routes and finding the most efficient transportation options."""),
            goal=dedent(f"""Plan optimal transportation routes, suggest the best travel methods, provide public transit information, 
                        and estimate accurate travel times between locations for the traveler's itinerary."""),
            tools=[
                SearchTools.search_internet,
                CalculatorTools.calculate,
                TravelTools.get_transportation_routes,
                TravelTools.calculate_travel_budget
            ],
            verbose=True,
            llm=self.llm,
        )

    def accommodation_expert(self):
        return Agent(
            role="Accommodation Expert",
            backstory=dedent(f"""I am a seasoned accommodation specialist with years of experience in the hospitality industry. 
                             I have deep knowledge of various lodging options, neighborhoods, and booking strategies worldwide."""),
            goal=dedent(f"""Recommend the best hotels and rentals, suggest ideal neighborhoods to stay in, provide booking tips, 
                        and analyze accommodation reviews to ensure the best stay for travelers."""),
            tools=[
                SearchTools.search_internet,
                TravelTools.get_accommodation_options,
                TravelTools.calculate_travel_budget,
                TravelTools.get_safety_information
            ],
            verbose=True,
            llm=self.llm,
        )

    def food_dining_guide(self):
        return Agent(
            role="Food & Dining Guide",
            backstory=dedent(f"""I am a culinary expert and food tour specialist with extensive knowledge of global cuisines, 
                             local specialties, and dietary requirements. I have experience in creating memorable food experiences."""),
            goal=dedent(f"""Recommend the best restaurants, suggest local specialties, provide dietary restriction information, 
                        and create comprehensive food tour itineraries that showcase the destination's culinary scene."""),
            tools=[
                SearchTools.search_internet,
                TravelTools.get_restaurant_recommendations,
                TravelTools.get_local_events,
                TravelTools.calculate_travel_budget
            ],
            verbose=True,
            llm=self.llm,
        )

    def travel_planning_expert(self) -> Agent:
        """Create an agent for travel planning"""
        return Agent(
            role="Travel Planning Expert",
            goal="Create detailed travel plans and itineraries",
            backstory="""You are a seasoned travel planner with years of experience creating
            personalized travel itineraries. You excel at balancing activities, managing budgets,
            and ensuring travelers have memorable experiences.""",
            verbose=True,
            llm=self.llm,
            tools=[
                Tool(
                    name="search_internet",
                    func=SearchTools.search_internet,
                    description="Search the internet for travel information and recommendations"
                ),
                Tool(
                    name="get_weather_forecast",
                    func=TravelTools.get_weather_forecast,
                    description="Get weather forecast for a destination"
                ),
                Tool(
                    name="get_local_events",
                    func=TravelTools.get_local_events,
                    description="Get local events for a destination"
                ),
                Tool(
                    name="calculate_travel_budget",
                    func=TravelTools.calculate_travel_budget,
                    description="Calculate estimated travel budget for a destination"
                )
            ],
            output_format={
                "type": "json",
                "schema": {
                    "itinerary": [
                        {
                            "day": "number",
                            "date": "string",
                            "activities": [
                                {
                                    "time": "string",
                                    "activity": "string",
                                    "description": "string",
                                    "location": "string",
                                    "duration": "string",
                                    "cost": "number"
                                }
                            ],
                            "meals": [
                                {
                                    "time": "string",
                                    "type": "string",
                                    "suggestion": "string",
                                    "cost": "number"
                                }
                            ]
                        }
                    ],
                    "budget_breakdown": {
                        "accommodation": "number",
                        "food": "number",
                        "activities": "number",
                        "transportation": "number",
                        "total": "number"
                    },
                    "recommendations": ["string"]
                }
            }
        )

    def budget_planner(self) -> Agent:
        """Create an agent for budget planning"""
        return Agent(
            role="Budget Planning Expert",
            goal="Create and manage travel budgets",
            backstory="""You are a financial expert specializing in travel budgets.
            You help travelers make the most of their money while ensuring they have
            a comfortable and enjoyable trip.""",
            verbose=True,
            llm=self.llm,
            tools=[
                Tool(
                    name="calculate_travel_budget",
                    func=TravelTools.calculate_travel_budget,
                    description="Calculate estimated travel budget for a destination"
                ),
                Tool(
                    name="calculate",
                    func=CalculatorTools.calculate,
                    description="Perform calculations for budget planning"
                )
            ],
            output_format={
                "type": "json",
                "schema": {
                    "budget_breakdown": {
                        "accommodation": "number",
                        "food": "number",
                        "activities": "number",
                        "transportation": "number",
                        "total": "number"
                    },
                    "savings_tips": ["string"],
                    "splurge_recommendations": ["string"]
                }
            }
        )

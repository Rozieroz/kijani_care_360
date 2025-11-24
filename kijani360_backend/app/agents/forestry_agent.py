import os
from typing import Dict, List, Optional
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser
from app.core.config import settings

class ForestryAgent:
    def __init__(self):
        self.llm = None
        self.knowledge_base = self._load_knowledge_base()
        self._initialize_llm()
    
    def _initialize_llm(self):
        """Initialize the Groq LLM"""
        if settings.GROQ_API_KEY:
            try:
                self.llm = ChatGroq(
                    groq_api_key=settings.GROQ_API_KEY,
                    model_name="openai/gpt-oss-120b",
                    temperature=0.3,
                    max_tokens=1024
                )
            except Exception as e:
                print(f"Failed to initialize Groq LLM: {e}")
                self.llm = None
    
    def _load_knowledge_base(self) -> str:
        """Load forestry knowledge base"""
        return """
        You are an expert forestry consultant specializing in tree conservation in Kenya. 
        
        KENYAN TREE SPECIES DATABASE:
        
        1. **Grevillea robusta (Silky Oak)**
           - Survival Rates: Coast (75%), Central (90%), Western (85%), Eastern (70%), Northern (60%), Rift Valley (88%)
           - Best Regions: Central Kenya, Western Kenya, Rift Valley
           - Intercropping: Excellent with coffee, tea, maize, beans
           - Growth: Fast (2-3m/year), mature height 15-30m
           - Water: Moderate requirements, drought tolerant when established
           - Soil: Well-drained, fertile soils, pH 5.5-7.0
           - Benefits: Timber, firewood, windbreak, erosion control
           - Planting: Best during rainy seasons (March-May, October-December)
        
        2. **Melia volkensii (Mukau)**
           - Survival Rates: Coast (95%), Central (70%), Western (65%), Eastern (95%), Northern (90%), Rift Valley (80%)
           - Best Regions: Eastern Kenya, Northern Kenya, Coast (arid/semi-arid)
           - Intercropping: Good with drought-resistant crops (sorghum, millet, cowpeas)
           - Growth: Medium to fast, mature height 10-20m
           - Water: Very low requirements, extremely drought tolerant
           - Soil: Adapts to poor soils, sandy, rocky soils
           - Benefits: High-value timber, medicinal bark, honey production
           - Planting: Any time, but best at start of rains
        
        3. **Croton megalocarpus (Musine)**
           - Survival Rates: Coast (60%), Central (85%), Western (80%), Eastern (65%), Northern (50%), Rift Valley (82%)
           - Best Regions: Central Kenya, Western Kenya, parts of Rift Valley
           - Intercropping: Compatible with coffee, bananas, vegetables, maize
           - Growth: Fast growing, mature height 15-25m
           - Water: Moderate requirements
           - Soil: Well-drained soils, pH 6.0-7.5
           - Benefits: Biodiesel production, timber, soil improvement, carbon sequestration
           - Planting: Rainy seasons for best establishment
        
        4. **Markhamia lutea (Siala)**
           - Survival Rates: Coast (80%), Central (88%), Western (90%), Eastern (75%), Northern (65%), Rift Valley (85%)
           - Best Regions: Widespread across Kenya, very adaptable
           - Intercropping: Excellent for agroforestry, compatible with most crops
           - Growth: Fast growing, mature height 10-20m
           - Water: Moderate requirements, fairly drought tolerant
           - Soil: Various soil types, pH 5.5-7.5
           - Benefits: Timber, poles, medicinal uses, bee forage
           - Planting: Rainy seasons preferred
        
        5. **Acacia species (various)**
           - Survival Rates: Coast (85%), Central (70%), Western (75%), Eastern (90%), Northern (95%), Rift Valley (88%)
           - Best Regions: Northern Kenya, Eastern Kenya, Rift Valley (arid areas)
           - Intercropping: Nitrogen fixation benefits crops, good with cereals and legumes
           - Growth: Fast in arid conditions, height varies by species
           - Water: Very low requirements, extreme drought tolerance
           - Soil: Poor soils, saline soils, various pH levels
           - Benefits: Fodder, gum arabic, soil improvement, erosion control
           - Planting: Start of rainy season or dry season planting possible
        
        6. **Prunus africana (Red Stinkwood)**
           - Survival Rates: Coast (40%), Central (75%), Western (70%), Eastern (45%), Northern (30%), Rift Valley (65%)
           - Best Regions: Central Kenya highlands, Mt. Kenya, Aberdares (above 1500m)
           - Intercropping: Shade-tolerant crops, coffee under canopy
           - Growth: Slow to medium, mature height 20-40m
           - Water: High requirements, needs consistent moisture
           - Soil: Rich, moist highland soils, pH 5.0-6.5
           - Benefits: Medicinal bark (prostate treatment), high conservation value
           - Planting: Rainy seasons, requires nursery care
        
        7. **Terminalia brownii (Muuku)**
           - Survival Rates: Coast (70%), Central (60%), Western (55%), Eastern (85%), Northern (80%), Rift Valley (75%)
           - Best Regions: Eastern Kenya, parts of Rift Valley (semi-arid)
           - Intercropping: Good with sorghum, millet, drought-resistant crops
           - Growth: Medium growth rate, mature height 8-15m
           - Water: Low to moderate requirements
           - Soil: Various soil types, drought conditions
           - Benefits: Timber, medicinal uses, fodder, erosion control
           - Planting: Start of rainy season
        
        8. **Casuarina equisetifolia (Casuarina)**
           - Survival Rates: Coast (90%), Central (70%), Western (65%), Eastern (75%), Northern (70%), Rift Valley (72%)
           - Best Regions: Coastal areas, saline soils
           - Intercropping: Limited due to allelopathic effects, good windbreak
           - Growth: Very fast, mature height 15-35m
           - Water: Moderate requirements, salt tolerant
           - Soil: Sandy soils, saline soils, pH 6.0-8.0
           - Benefits: Windbreak, erosion control, firewood, poles
           - Planting: Any season, very hardy
        
        REGIONAL CLIMATE ZONES:
        - Coast: Hot, humid, two rainy seasons, saline soils
        - Central: Temperate, high altitude, fertile soils, reliable rainfall
        - Western: High rainfall, fertile soils, good for agriculture
        - Eastern: Semi-arid, low rainfall, drought-prone
        - Northern: Arid, very low rainfall, harsh conditions
        - Rift Valley: Varied climate, from arid to temperate depending on altitude
        
        INTERCROPPING GUIDELINES:
        - Consider tree spacing (minimum 10m for large trees)
        - Match water and nutrient requirements
        - Consider shade tolerance of crops
        - Plan for tree growth and canopy development
        - Nitrogen-fixing trees benefit companion crops
        
        SURVIVAL FACTORS:
        - Soil preparation and quality
        - Planting timing (rainy season preferred)
        - Seedling quality and age
        - Post-planting care and protection
        - Local climate variations
        - Pest and disease management
        
        Always provide specific, practical advice based on user's location, goals, and conditions.
        Include survival rates, best practices, and regional considerations.
        """
    
    def query(self, question: str, context: Optional[Dict] = None) -> str:
        """Query the forestry agent with a question"""
        if not self.llm:
            return self._fallback_response(question)
        
        try:
            # Create context-aware prompt
            context_str = ""
            if context:
                if context.get("region"):
                    context_str += f"User is in {context['region']} region of Kenya. "
                if context.get("soil_type"):
                    context_str += f"Soil type: {context['soil_type']}. "
                if context.get("rainfall"):
                    context_str += f"Annual rainfall: {context['rainfall']}mm. "
            
            prompt = ChatPromptTemplate.from_messages([
                ("system", self.knowledge_base),
                ("human", f"{context_str}Question: {question}")
            ])
            
            chain = (
                {"question": RunnablePassthrough()}
                | prompt
                | self.llm
                | StrOutputParser()
            )
            
            response = chain.invoke(question)
            return response
            
        except Exception as e:
            print(f"Error querying LLM: {e}")
            return self._fallback_response(question)
    
    def _fallback_response(self, question: str) -> str:
        """Provide fallback responses when LLM is not available"""
        question_lower = question.lower()
        
        if "grevillea" in question_lower:
            return """Grevillea robusta (Silky Oak) is excellent for Central Kenya and Rift Valley with 90% and 88% survival rates respectively. 
            It's perfect for intercropping with coffee, tea, and maize. Fast-growing (2-3m/year) and provides timber, firewood, and windbreak benefits. 
            Plant during rainy seasons in well-drained, fertile soils."""
        
        elif any(region in question_lower for region in ["central", "central kenya"]):
            return """Best trees for Central Kenya: Grevillea robusta (90% survival), Markhamia lutea (88% survival), 
            and Croton megalocarpus (85% survival). All excellent for intercropping with coffee and vegetables. 
            The region's fertile soils and reliable rainfall support most tree species well."""
        
        elif "intercrop" in question_lower or "agroforestry" in question_lower:
            return """Top intercropping trees: Grevillea robusta (coffee, tea, maize), Croton megalocarpus (coffee, bananas, vegetables), 
            and Markhamia lutea (excellent for agroforestry systems). Acacia species also fix nitrogen benefiting companion crops. 
            Maintain 10m spacing for large trees."""
        
        elif any(word in question_lower for word in ["drought", "dry", "arid", "eastern", "northern"]):
            return """Best drought-resistant trees: Melia volkensii (95% survival in Eastern Kenya), Acacia species (90-95% survival in arid areas), 
            and Terminalia brownii (85% survival in Eastern Kenya). These thrive in low rainfall areas and poor soils."""
        
        elif "coast" in question_lower or "coastal" in question_lower:
            return """Coastal region trees: Melia volkensii (95% survival), Casuarina equisetifolia (90% survival), 
            and Markhamia lutea (80% survival) perform well. Consider salt tolerance and sandy soils when selecting species."""
        
        elif "survival rate" in question_lower:
            return """Survival rates vary by region. Highest performers: Melia volkensii in arid areas (90-95%), 
            Grevillea robusta in Central/Rift Valley (88-90%), Acacia species in Northern Kenya (95%). 
            Success depends on proper site selection, timing, and post-planting care."""
        
        else:
            return """I can help with tree species selection, survival rates across Kenya's regions, intercropping advice, 
            and forestry best practices. Ask about specific trees like Grevillea, Melia, or Croton, or about planting 
            in specific regions like Central, Eastern, or Coastal Kenya."""
    
    def get_species_recommendation(self, region: str, purpose: str, soil_type: str = None) -> Dict:
        """Get tree species recommendations based on criteria"""
        recommendations = {
            "central": {
                "timber": ["Grevillea robusta", "Croton megalocarpus", "Markhamia lutea"],
                "agroforestry": ["Grevillea robusta", "Markhamia lutea", "Croton megalocarpus"],
                "erosion_control": ["Grevillea robusta", "Markhamia lutea"],
                "general": ["Grevillea robusta", "Markhamia lutea", "Croton megalocarpus"]
            },
            "eastern": {
                "drought_tolerance": ["Melia volkensii", "Terminalia brownii", "Acacia species"],
                "agroforestry": ["Melia volkensii", "Acacia species"],
                "general": ["Melia volkensii", "Terminalia brownii", "Markhamia lutea"]
            },
            "coast": {
                "salt_tolerance": ["Casuarina equisetifolia", "Melia volkensii"],
                "windbreak": ["Casuarina equisetifolia", "Grevillea robusta"],
                "general": ["Melia volkensii", "Casuarina equisetifolia", "Markhamia lutea"]
            }
        }
        
        region_recs = recommendations.get(region.lower(), recommendations["central"])
        species_list = region_recs.get(purpose.lower(), region_recs.get("general", []))
        
        return {
            "recommended_species": species_list,
            "region": region,
            "purpose": purpose,
            "note": f"Recommendations for {purpose} in {region} region of Kenya"
        }
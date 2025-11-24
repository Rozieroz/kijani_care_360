from typing import Dict, List, Optional
import os
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser
from langchain.memory import ConversationBufferWindowMemory
from langchain.schema import HumanMessage, SystemMessage, AIMessage
from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.models.tree import TreeSpecies
from app.models.forum import ChatHistory
from datetime import datetime

class KenyaTreeExpertBot:
    def __init__(self, db: Session):
        self.db = db
        self.knowledge_base = self._load_tree_knowledge()
        self.groq_available = self._check_groq_availability()
        
    def _load_tree_knowledge(self) -> str:
        """Load comprehensive tree knowledge from database and static data"""
        # Get tree data from database
        trees = self.db.query(TreeSpecies).all()
        
        db_knowledge = "\n".join([
            f"- {tree.name} ({tree.local_name}): "
            f"Growth: {tree.growth_rate}. Water: {tree.water_requirements}. "
            f"Climate: {tree.climate_zones}. "
            f"Benefits: Timber={tree.timber_value}, Fruit={tree.fruit_bearing}, Medicinal={tree.medicinal_uses}"
            for tree in trees
        ])
        
        static_knowledge = """
        You are KijaniBot, an expert on tree species in Kenya and sustainable forestry practices.
        
        COMPREHENSIVE TREE KNOWLEDGE:
        
        1. **Grevillea robusta (Silky Oak/Mukima)**
           - Survival Rate: 80-90% in Central Kenya, Rift Valley, Western Kenya
           - Best Regions: Central highlands (1500-2500m altitude)
           - Intercropping: Excellent with coffee, tea, maize, beans
           - Growth: Fast-growing (2-3m/year), reaches 15-30m
           - Benefits: Timber, firewood, windbreak, soil conservation
           - Soil: Well-drained, fertile soils, pH 5.5-7.0
           - Rainfall: 1000-2000mm annually
        
        2. **Melia volkensii (Mukau)**
           - Survival Rate: 85-95% in arid/semi-arid areas
           - Best Regions: Eastern Kenya, Coast, Machakos, Kitui
           - Intercropping: Compatible with drought-resistant crops (sorghum, millet, cowpeas)
           - Growth: Medium to fast (1-2m/year), drought-resistant
           - Benefits: High-value timber, medicinal bark, honey production
           - Soil: Adapts to various soils, tolerates poor drainage
           - Rainfall: 400-1200mm annually
        
        3. **Croton megalocarpus (Musine/Mukinduri)**
           - Survival Rate: 75-85% in highlands
           - Best Regions: Central Kenya, Western Kenya, parts of Rift Valley
           - Intercropping: Good with coffee, bananas, vegetables, legumes
           - Growth: Fast-growing, nitrogen-fixing
           - Benefits: Biodiesel production, timber, soil improvement
           - Soil: Well-drained soils, pH 6.0-7.5
           - Rainfall: 1000-1800mm annually
        
        4. **Markhamia lutea (Siala/Muu)**
           - Survival Rate: 80-90% across Kenya
           - Best Regions: Widespread - Central, Western, Coast, Nyanza
           - Intercropping: Excellent for agroforestry systems
           - Growth: Fast-growing, adaptable
           - Benefits: Timber, poles, medicinal uses, bee forage
           - Soil: Various soil types, tolerates waterlogging
           - Rainfall: 800-2000mm annually
        
        5. **Acacia species (Mgunga/Mti wa miba)**
           - Survival Rate: 85-95% in dry areas
           - Best Regions: Northern Kenya, Eastern Kenya, Rift Valley
           - Intercropping: Fixes nitrogen, good with cereals and legumes
           - Growth: Fast in arid conditions, drought-tolerant
           - Benefits: Fodder, gum arabic, soil improvement, charcoal
           - Soil: Poor soils, sandy, rocky areas
           - Rainfall: 200-800mm annually
        
        6. **Prunus africana (Red Stinkwood/Muiri)**
           - Survival Rate: 60-75% in highlands
           - Best Regions: Central Kenya highlands, Mt. Kenya, Aberdares
           - Intercropping: Compatible with shade-tolerant crops
           - Growth: Slow to medium, high conservation value
           - Benefits: Medicinal bark (prostate treatment), timber
           - Soil: Rich, moist highland soils
           - Rainfall: 1200-2500mm annually
        
        7. **Terminalia brownii (Muuku)**
           - Survival Rate: 80-90% in dry areas
           - Best Regions: Eastern Kenya, parts of Rift Valley
           - Intercropping: Good with sorghum, millet, drought-tolerant crops
           - Growth: Medium, drought-resistant
           - Benefits: Timber, medicinal, fodder, soil conservation
           - Soil: Various soil types, drought-tolerant
           - Rainfall: 400-1000mm annually
        
        8. **Casuarina equisetifolia (Mvinje)**
           - Survival Rate: 90-95% in coastal areas
           - Best Regions: Coast, saline soils
           - Intercropping: Windbreak for crops, nitrogen-fixing
           - Growth: Very fast-growing
           - Benefits: Windbreak, fuelwood, soil stabilization
           - Soil: Tolerates saline and sandy soils
           - Rainfall: 600-1500mm annually
        
        REGIONAL RECOMMENDATIONS:
        - Central Kenya: Grevillea, Croton, Prunus africana
        - Western Kenya: Grevillea, Markhamia, Croton
        - Eastern Kenya: Melia volkensii, Terminalia, Acacia
        - Coast: Casuarina, Markhamia, Melia volkensii
        - Rift Valley: Grevillea, Acacia, Terminalia
        - Northern Kenya: Acacia species, drought-resistant varieties
        
        INTERCROPPING GUIDELINES:
        - Coffee: Grevillea robusta (traditional), Croton megalocarpus
        - Tea: Grevillea robusta for windbreak
        - Maize: Grevillea, Markhamia (proper spacing)
        - Vegetables: Croton, Markhamia (light shade)
        - Legumes: Most trees (nitrogen cycling)
        
        CLIMATE CONSIDERATIONS:
        - High rainfall (>1200mm): Grevillea, Prunus, Croton
        - Medium rainfall (800-1200mm): Markhamia, Terminalia
        - Low rainfall (<800mm): Melia volkensii, Acacia species
        
        Always provide specific, practical advice based on user's location, climate, and farming system.
        """
        
        return static_knowledge + "\n\nDATABASE TREES:\n" + db_knowledge
    
    def get_chatbot_chain(self):
        """Initialize the LangChain chatbot with Groq"""
        api_key = os.getenv("GROQ_API_KEY")
        
        if not api_key or api_key == "your_groq_api_key_here":
            raise ValueError("GROQ_API_KEY not configured")
        
        # Initialize Groq LLM
        llm = ChatGroq(
            groq_api_key=api_key,
            model_name="openai/gpt-oss-20b",
            temperature=0.3,
            max_tokens=1024
        )
        
        # Create prompt template
        prompt = ChatPromptTemplate.from_messages([
            ("system", self.knowledge_base),
            ("human", "{question}")
        ])
        
        # Create chain
        chain = (
            {"question": RunnablePassthrough()}
            | prompt
            | llm
            | StrOutputParser()
        )
        
        return chain
    
    def _check_groq_availability(self) -> bool:
        """Check if Groq API is available and configured"""
        # Load environment variables
        from dotenv import load_dotenv
        load_dotenv()
        
        api_key = os.getenv("GROQ_API_KEY")
        return api_key and api_key != "your_groq_api_key_here" and len(api_key) > 20
    
    def _get_conversation_history(self, user_id: int, limit: int = 5) -> List[Dict]:
        """Get recent conversation history for context"""
        history = self.db.query(ChatHistory).filter(
            ChatHistory.user_id == user_id
        ).order_by(desc(ChatHistory.created_at)).limit(limit).all()
        
        # Return in chronological order (oldest first)
        return [
            {"question": h.question, "answer": h.answer}
            for h in reversed(history)
        ]
    
    def get_response(self, question: str, user_id: int) -> Dict[str, any]:
        """Get AI response to user question with conversation memory"""
        
        # Get conversation history for context
        conversation_history = self._get_conversation_history(user_id)
        
        if self.groq_available:
            try:
                # Use Groq LLM with conversation context
                answer = self._get_groq_response(question, conversation_history)
                confidence = "high"
                sources = ["Kenya Forest Service", "ICRAF Agroforestry Database", "KijaniCare360 AI"]
                note = "Powered by Groq AI"
                
            except Exception as e:
                print(f"Groq API error: {e}")
                # Fallback to rule-based response
                answer = self._get_fallback_response(question, conversation_history)
                confidence = "medium"
                sources = ["KijaniCare360 Knowledge Base"]
                note = "Using fallback response due to AI service issue"
        else:
            # Use fallback response
            answer = self._get_fallback_response(question, conversation_history)
            confidence = "medium"
            sources = ["KijaniCare360 Knowledge Base"]
            note = "Groq API not configured, using built-in responses"
        
        # Save to chat history
        try:
            chat_record = ChatHistory(
                user_id=user_id,
                question=question,
                answer=answer,
                created_at=datetime.utcnow()
            )
            self.db.add(chat_record)
            self.db.commit()
        except Exception as e:
            print(f"Error saving chat history: {e}")
        
        return {
            "answer": answer,
            "sources": sources,
            "confidence": confidence,
            "note": note
        }
    
    def _get_groq_response(self, question: str, conversation_history: List[Dict]) -> str:
        """Get response from Groq LLM with conversation context and rich formatting"""
        api_key = os.getenv("GROQ_API_KEY")
        
        # Initialize Groq LLM with current working model
        llm = ChatGroq(
            groq_api_key=api_key,
            model_name="llama-3.1-8b-instant",  # Current working model
            temperature=0.3,
            max_tokens=1024
        )
        
        # Enhanced system prompt with formatting instructions
        enhanced_knowledge = self.knowledge_base + """
        
        RESPONSE FORMATTING GUIDELINES:
        - Use **bold text** for important tree names, key benefits, and critical information
        - Use *italic text* for scientific names, emphasis, and regional names
        - Use bullet points (•) for lists and multiple items
        - Use numbered lists (1., 2., 3.) for step-by-step instructions
        - Structure responses with clear sections using **headings**
        - Always be specific with survival rates, regions, and practical advice
        - Include emojis where appropriate: 🌳 for trees, 🌱 for planting, 💧 for water, 🌍 for regions
        
        Example formatting:
        **Grevillea robusta** (*Silky Oak/Mukima*) is excellent for *Central Kenya*:
        
        **Key Benefits:**
        • **Survival Rate:** 80-90% in highlands
        • **Growth:** Fast-growing (2-3m/year)
        • **Uses:** Timber, windbreak, soil conservation
        
        **Planting Instructions:**
        1. **Site Selection:** Well-drained soils, pH 5.5-7.0
        2. **Spacing:** 6-8 meters for intercropping
        3. **Season:** Plant during long rains (March-May)
        
        Always format your responses this way for better readability.
        """
        
        # Build conversation context
        messages = [SystemMessage(content=enhanced_knowledge)]
        
        # Add conversation history
        for exchange in conversation_history:
            messages.append(HumanMessage(content=exchange["question"]))
            messages.append(AIMessage(content=exchange["answer"]))
        
        # Add current question with formatting request
        formatted_question = f"{question}\n\nPlease format your response with **bold** for important information and *italics* for emphasis."
        messages.append(HumanMessage(content=formatted_question))
        
        # Get response
        response = llm.invoke(messages)
        return response.content
    
    def _get_fallback_response(self, question: str, conversation_history: List[Dict] = None) -> str:
        """Provide rule-based responses when AI is unavailable"""
        question_lower = question.lower()
        
        # Check for follow-up questions based on conversation history
        if conversation_history:
            last_exchange = conversation_history[-1] if conversation_history else None
            if last_exchange and ("more" in question_lower or "tell me" in question_lower or "what about" in question_lower):
                # This seems like a follow-up question
                if "grevillea" in last_exchange["answer"].lower():
                    return ("Grevillea robusta grows 2-3 meters per year and can reach 15-30m at maturity. "
                           "It's excellent for windbreaks and can be harvested for timber after 8-12 years. "
                           "The leaves provide good mulch and the tree fixes nitrogen in soil.")
                elif "melia" in last_exchange["answer"].lower():
                    return ("Melia volkensii is particularly valuable because it produces high-quality timber "
                           "that's resistant to termites. It can survive on as little as 400mm of rainfall per year "
                           "and is excellent for dryland farming systems.")
                elif "central kenya" in last_exchange["answer"].lower():
                    return ("In Central Kenya, plant trees during the long rains (March-May) for best survival. "
                           "Space Grevillea 6-8 meters apart when intercropping with coffee. "
                           "The altitude of 1500-2500m in Central Kenya is perfect for most highland species.")
        
        # Check for clarification requests
        if any(word in question_lower for word in ["clarify", "explain", "what do you mean", "more details"]):
            if conversation_history:
                return ("I'd be happy to clarify! Could you be more specific about which part you'd like me to explain further? "
                       "For example, are you asking about planting techniques, survival rates, or intercropping methods?")
        
        
        # Tree species queries with rich formatting
        if "grevillea" in question_lower:
            return ("🌳 **Grevillea robusta** (*Silky Oak/Mukima*) is excellent for *Central Kenya* and *Rift Valley*:\n\n"
                   "**Survival Rate:** 80-90% in highlands\n"
                   "**Best For:** Intercropping with coffee, tea, and maize\n"
                   "**Growth:** Fast-growing (2-3m/year)\n"
                   "**Benefits:** Timber, firewood, windbreak, soil conservation\n\n"
                   "*Perfect choice for highland agroforestry systems!* 🌱")
        
        elif "melia" in question_lower or "mukau" in question_lower:
            return ("🌳 **Melia volkensii** (*Mukau*) - the drought champion:\n\n"
                   "**Survival Rate:** 85-95% in arid areas\n"
                   "**Best Regions:** *Eastern Kenya*, *Machakos*, *Kitui*\n"
                   "**Drought Tolerance:** Excellent (400-1200mm rainfall)\n"
                   "**Intercropping:** Compatible with sorghum, millet, cowpeas\n"
                   "**Special Value:** High-quality, termite-resistant timber\n\n"
                   "*Ideal for dryland farming systems!* 🌵")
        
        elif "croton" in question_lower:
            return ("🌳 **Croton megalocarpus** (*Musine/Mukinduri*) - the multi-purpose tree:\n\n"
                   "**Survival Rate:** 75-85% in highlands\n"
                   "**Best Regions:** *Central Kenya*, *Western Kenya*\n"
                   "**Special Feature:** Nitrogen-fixing capabilities\n"
                   "**Intercropping:** Coffee, bananas, vegetables, legumes\n"
                   "**Unique Benefit:** Biodiesel production from seeds\n\n"
                   "*Great for soil improvement and renewable energy!* ⚡")
        
        # Regional queries with rich formatting
        elif "central kenya" in question_lower:
            return ("🌍 **Best Trees for Central Kenya** (1500-2500m altitude):\n\n"
                   "1. **Grevillea robusta** - 80-90% survival rate\n"
                   "   • *Perfect for coffee intercropping*\n"
                   "   • Fast-growing windbreak\n\n"
                   "2. **Croton megalocarpus** - 75-85% survival rate\n"
                   "   • *Nitrogen-fixing capabilities*\n"
                   "   • Biodiesel production\n\n"
                   "3. **Prunus africana** - 60-75% survival rate\n"
                   "   • *High conservation value*\n"
                   "   • Medicinal bark benefits\n\n"
                   "**Best Planting Season:** March-May (long rains) 🌧️")
        
        elif "eastern kenya" in question_lower or "arid" in question_lower:
            return ("🌵 **Drought-Resistant Trees for Eastern Kenya:**\n\n"
                   "**Top Performers:**\n"
                   "• **Melia volkensii** - 85-95% survival\n"
                   "• **Acacia species** - 85-95% survival\n"
                   "• **Terminalia brownii** - 80-90% survival\n\n"
                   "**Rainfall Tolerance:** 200-800mm annually\n"
                   "**Best Counties:** *Machakos*, *Kitui*, *Makueni*, *Tharaka-Nithi*\n\n"
                   "*These trees thrive where others fail!* 💪")
        
        elif "coast" in question_lower or "coastal" in question_lower:
            return ("🏖️ **Coastal Region Tree Recommendations:**\n\n"
                   "**Salt-Tolerant Champions:**\n"
                   "• **Casuarina equisetifolia** (*Mvinje*)\n"
                   "  - 90-95% survival in saline soils\n"
                   "  - Excellent windbreak properties\n\n"
                   "• **Markhamia lutea** (*Siala*)\n"
                   "  - Adaptable to coastal conditions\n"
                   "  - Multiple uses: timber, poles, medicine\n\n"
                   "• **Melia volkensii**\n"
                   "  - Drought and salt tolerant\n\n"
                   "**Special Benefit:** Protection from ocean winds 🌊")
        
        # Intercropping queries
        elif "coffee" in question_lower and "intercrop" in question_lower:
            return ("Best trees for coffee intercropping: Grevillea robusta (traditional choice) "
                   "and Croton megalocarpus. Both provide shade, windbreak, and additional income "
                   "while improving soil fertility.")
        
        elif "intercrop" in question_lower or "agroforestry" in question_lower:
            return ("Top intercropping trees: Grevillea robusta (coffee, tea, maize), "
                   "Croton megalocarpus (coffee, bananas, vegetables), Markhamia lutea "
                   "(excellent for agroforestry), and Acacia species (nitrogen-fixing).")
        
        # Survival rate queries
        elif "survival rate" in question_lower:
            return ("Tree survival rates in Kenya: Acacia species (85-95% in dry areas), "
                   "Melia volkensii (85-95% arid), Grevillea robusta (80-90% highlands), "
                   "Markhamia lutea (80-90% widespread). Choose based on your region's climate.")
        
        # Default response
        else:
            return ("I have information on 8+ tree species for Kenya including Grevillea robusta, "
                   "Melia volkensii, Croton megalocarpus, and more. I can help with survival rates, "
                   "regional suitability, intercropping compatibility, and planting advice. "
                   "What specific information do you need?")
    
    def get_tree_recommendations(self, region: str, rainfall: int, farming_system: str) -> List[Dict]:
        """Get personalized tree recommendations"""
        recommendations = []
        
        # Query database for suitable trees
        suitable_trees = self.db.query(TreeSpecies).filter(
            TreeSpecies.climate_zones.ilike(f"%{region}%")
        ).all()
        
        for tree in suitable_trees:
            score = self._calculate_suitability_score(tree, region, rainfall, farming_system)
            recommendations.append({
                "species_name": tree.name,
                "local_name": tree.local_name,
                "survival_rate": self._get_regional_survival_rate(tree, region),
                "suitability_score": score,
                "benefits": f"Timber: {tree.timber_value}, Fruit: {tree.fruit_bearing}, Medicinal: {tree.medicinal_uses}",
                "intercropping": tree.water_requirements
            })
        
        # Sort by suitability score
        recommendations.sort(key=lambda x: x["suitability_score"], reverse=True)
        return recommendations[:5]  # Top 5 recommendations
    
    def _calculate_suitability_score(self, tree: TreeSpecies, region: str, rainfall: int, farming_system: str) -> float:
        """Calculate suitability score for a tree based on conditions"""
        base_score = self._get_regional_survival_rate(tree, region)
        
        # Adjust for water requirements
        if tree.water_requirements:
            if rainfall > 1200 and tree.water_requirements.lower() == "high":
                base_score += 10
            elif 600 <= rainfall <= 1200 and tree.water_requirements.lower() == "medium":
                base_score += 10
            elif rainfall < 600 and tree.water_requirements.lower() == "low":
                base_score += 10
            else:
                base_score -= 10
        
        # Climate zone bonus
        if tree.climate_zones and region.lower() in tree.climate_zones.lower():
            base_score += 15
        
        return min(100, max(0, base_score))  # Clamp between 0-100
    
    def _get_regional_survival_rate(self, tree: TreeSpecies, region: str) -> float:
        """Get survival rate for specific region"""
        region_lower = region.lower()
        if "central" in region_lower and tree.survival_rate_central:
            return tree.survival_rate_central
        elif "western" in region_lower and tree.survival_rate_western:
            return tree.survival_rate_western
        elif "eastern" in region_lower and tree.survival_rate_eastern:
            return tree.survival_rate_eastern
        elif "coast" in region_lower and tree.survival_rate_coast:
            return tree.survival_rate_coast
        elif "rift" in region_lower and tree.survival_rate_rift_valley:
            return tree.survival_rate_rift_valley
        elif "northern" in region_lower and tree.survival_rate_northern:
            return tree.survival_rate_northern
        else:
            # Return average of available rates
            rates = [
                tree.survival_rate_central, tree.survival_rate_western,
                tree.survival_rate_eastern, tree.survival_rate_coast,
                tree.survival_rate_rift_valley, tree.survival_rate_northern
            ]
            valid_rates = [r for r in rates if r is not None]
            return sum(valid_rates) / len(valid_rates) if valid_rates else 70.0
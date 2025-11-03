"""
Cooking AI Agent Application
A smart cooking assistant powered by GitHub models that helps with recipe search
and ingredient extraction using Microsoft Agent Framework.
"""

import asyncio
import os
from typing import Annotated
from agent_framework import ChatAgent
from agent_framework.openai import OpenAIChatClient
from openai import AsyncAzureOpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


# ============================================================
# Tool Definitions - Recipe Search and Ingredient Extraction
# ============================================================

def search_recipes(
    cuisine: Annotated[str, "The type of cuisine (e.g., Italian, Chinese, Mexican)"],
    difficulty: Annotated[str, "The difficulty level: easy, medium, or hard"] = "medium",
) -> str:
    """
    Search for recipes based on cuisine type and difficulty level.
    Returns a list of recipe suggestions with brief descriptions.
    """
    # Mock recipe database - in production, this would call a real recipe API
    recipes = {
        "italian": {
            "easy": [
                "Spaghetti Aglio e Olio - Simple pasta with garlic, olive oil, and red pepper flakes (20 min)",
                "Caprese Salad - Fresh tomatoes, mozzarella, basil, and balsamic glaze (10 min)",
                "Bruschetta - Toasted bread topped with tomatoes, garlic, and basil (15 min)",
            ],
            "medium": [
                "Chicken Parmigiana - Breaded chicken with tomato sauce and melted cheese (45 min)",
                "Risotto alla Milanese - Creamy saffron rice dish (40 min)",
                "Lasagna - Layered pasta with meat sauce, béchamel, and cheese (1.5 hours)",
            ],
            "hard": [
                "Osso Buco - Braised veal shanks with gremolata (3 hours)",
                "Homemade Ravioli - Fresh pasta filled with ricotta and spinach (2 hours)",
                "Tiramisu - Classic Italian dessert with coffee and mascarpone (2 hours + chilling)",
            ],
        },
        "chinese": {
            "easy": [
                "Egg Fried Rice - Simple rice with eggs, peas, and soy sauce (15 min)",
                "Stir-Fried Vegetables - Mixed vegetables with garlic and oyster sauce (20 min)",
                "Chinese Cucumber Salad - Refreshing cucumber with vinegar dressing (10 min)",
            ],
            "medium": [
                "Kung Pao Chicken - Spicy chicken with peanuts and vegetables (35 min)",
                "Sweet and Sour Pork - Crispy pork in tangy sauce (40 min)",
                "Mapo Tofu - Spicy tofu and ground pork in chili sauce (30 min)",
            ],
            "hard": [
                "Peking Duck - Crispy roasted duck with pancakes (4 hours)",
                "Dim Sum Dumplings - Steamed dumplings with various fillings (2 hours)",
                "Hot Pot - Interactive meal with various meats and vegetables (2 hours prep)",
            ],
        },
        "mexican": {
            "easy": [
                "Quesadillas - Cheese-filled tortillas, grilled until crispy (15 min)",
                "Guacamole - Mashed avocados with lime, cilantro, and onions (10 min)",
                "Nachos - Tortilla chips with cheese, salsa, and toppings (20 min)",
            ],
            "medium": [
                "Chicken Enchiladas - Rolled tortillas with chicken and cheese sauce (45 min)",
                "Tacos al Pastor - Marinated pork tacos with pineapple (1 hour)",
                "Chiles Rellenos - Stuffed poblano peppers with cheese (50 min)",
            ],
            "hard": [
                "Mole Poblano - Complex sauce with chocolate and chiles (3 hours)",
                "Tamales - Corn dough filled with meat, wrapped in corn husks (3 hours)",
                "Cochinita Pibil - Slow-roasted pork in citrus marinade (4 hours)",
            ],
        },
        "indian": {
            "easy": [
                "Dal Tadka - Lentil curry with spices (30 min)",
                "Raita - Yogurt sauce with cucumber and spices (10 min)",
                "Aloo Gobi - Cauliflower and potato curry (35 min)",
            ],
            "medium": [
                "Butter Chicken - Creamy tomato-based chicken curry (50 min)",
                "Chicken Biryani - Fragrant rice with spiced chicken (1 hour)",
                "Palak Paneer - Spinach curry with cottage cheese (40 min)",
            ],
            "hard": [
                "Rogan Josh - Complex lamb curry with aromatic spices (2.5 hours)",
                "Hyderabadi Biryani - Layered rice and meat dish (3 hours)",
                "Samosas from scratch - Fried pastries with spiced filling (2 hours)",
            ],
        },
    }
    
    cuisine_lower = cuisine.lower()
    difficulty_lower = difficulty.lower()
    
    if cuisine_lower not in recipes:
        available = ", ".join(recipes.keys())
        return f"Sorry, I don't have recipes for {cuisine} cuisine. Available cuisines: {available}"
    
    if difficulty_lower not in recipes[cuisine_lower]:
        return f"Invalid difficulty level. Please choose: easy, medium, or hard"
    
    recipe_list = recipes[cuisine_lower][difficulty_lower]
    result = f"Here are {difficulty} {cuisine} recipes:\n\n"
    for i, recipe in enumerate(recipe_list, 1):
        result += f"{i}. {recipe}\n"
    
    return result


def extract_ingredients(
    recipe_name: Annotated[str, "The name of the recipe to extract ingredients for"],
) -> str:
    """
    Extract and list all ingredients needed for a specific recipe.
    Returns detailed ingredient list with measurements.
    """
    # Mock ingredient database - in production, this would query a recipe database
    ingredients_db = {
        "spaghetti aglio e olio": {
            "ingredients": [
                "400g spaghetti pasta",
                "6 cloves garlic, thinly sliced",
                "1/2 cup extra virgin olive oil",
                "1 teaspoon red pepper flakes",
                "1/4 cup fresh parsley, chopped",
                "Salt to taste",
                "Freshly ground black pepper",
                "Parmesan cheese (optional, for serving)",
            ],
            "servings": "4 people",
            "prep_time": "5 minutes",
            "cook_time": "15 minutes",
        },
        "kung pao chicken": {
            "ingredients": [
                "500g chicken breast, diced",
                "2 tablespoons soy sauce",
                "1 tablespoon cornstarch",
                "3 tablespoons vegetable oil",
                "4 dried red chiles, cut into pieces",
                "1 teaspoon Sichuan peppercorns",
                "3 cloves garlic, minced",
                "1 tablespoon ginger, minced",
                "1 bell pepper, diced",
                "1/2 cup roasted peanuts",
                "3 green onions, chopped",
                "2 tablespoons rice vinegar",
                "1 tablespoon sugar",
                "1 tablespoon sesame oil",
            ],
            "servings": "4 people",
            "prep_time": "15 minutes",
            "cook_time": "20 minutes",
        },
        "butter chicken": {
            "ingredients": [
                "800g chicken thighs, cut into chunks",
                "1 cup plain yogurt",
                "2 tablespoons lemon juice",
                "2 teaspoons garam masala",
                "1 teaspoon turmeric",
                "1 teaspoon chili powder",
                "6 cloves garlic, minced",
                "2 tablespoons ginger, grated",
                "4 tablespoons butter",
                "1 large onion, diced",
                "400g canned tomatoes",
                "1 cup heavy cream",
                "1 tablespoon sugar",
                "Fresh cilantro for garnish",
                "Salt to taste",
            ],
            "servings": "6 people",
            "prep_time": "20 minutes (plus marinating time)",
            "cook_time": "30 minutes",
        },
        "chicken enchiladas": {
            "ingredients": [
                "3 cups cooked chicken, shredded",
                "8-10 flour or corn tortillas",
                "2 cups enchilada sauce",
                "2 cups shredded cheese (cheddar or Mexican blend)",
                "1/2 cup sour cream",
                "1 can black beans, drained",
                "1 bell pepper, diced",
                "1 onion, diced",
                "2 cloves garlic, minced",
                "1 teaspoon cumin",
                "1 teaspoon chili powder",
                "Fresh cilantro for garnish",
                "Lime wedges for serving",
            ],
            "servings": "4-6 people",
            "prep_time": "20 minutes",
            "cook_time": "25 minutes",
        },
        "caprese salad": {
            "ingredients": [
                "4 large ripe tomatoes, sliced",
                "400g fresh mozzarella cheese, sliced",
                "Fresh basil leaves",
                "1/4 cup extra virgin olive oil",
                "2 tablespoons balsamic vinegar or glaze",
                "Sea salt flakes",
                "Freshly ground black pepper",
            ],
            "servings": "4 people",
            "prep_time": "10 minutes",
            "cook_time": "0 minutes",
        },
    }
    
    recipe_lower = recipe_name.lower()
    
    # Try to find a matching recipe
    matched_recipe = None
    for key in ingredients_db:
        if key in recipe_lower or recipe_lower in key:
            matched_recipe = key
            break
    
    if not matched_recipe:
        return (f"Sorry, I don't have ingredient information for '{recipe_name}'. "
                f"Try asking about specific recipes like 'Spaghetti Aglio e Olio', "
                f"'Kung Pao Chicken', 'Butter Chicken', 'Chicken Enchiladas', or 'Caprese Salad'.")
    
    recipe_data = ingredients_db[matched_recipe]
    result = f"Ingredients for {matched_recipe.title()}:\n\n"
    result += f"Servings: {recipe_data['servings']}\n"
    result += f"Prep Time: {recipe_data['prep_time']}\n"
    result += f"Cook Time: {recipe_data['cook_time']}\n\n"
    result += "Ingredients:\n"
    
    for ingredient in recipe_data['ingredients']:
        result += f"• {ingredient}\n"
    
    return result


def get_cooking_tips(
    topic: Annotated[str, "The cooking topic or technique to get tips about"],
) -> str:
    """
    Get helpful cooking tips and techniques for various cooking topics.
    """
    tips_db = {
        "pasta": [
            "Always use a large pot with plenty of salted water (about 1 tablespoon salt per liter)",
            "Don't add oil to the pasta water - it prevents sauce from sticking",
            "Save some pasta water before draining - it helps create creamy sauces",
            "Taste pasta 1-2 minutes before the package time for perfect al dente texture",
            "Don't rinse pasta after cooking unless making a cold pasta salad",
        ],
        "rice": [
            "Rinse rice before cooking to remove excess starch for fluffier results",
            "Use a 1:2 ratio of rice to water for white rice, 1:2.5 for brown rice",
            "Let rice rest covered for 5-10 minutes after cooking for better texture",
            "Fluff with a fork, not a spoon, to avoid making it sticky",
            "Day-old refrigerated rice makes the best fried rice",
        ],
        "chicken": [
            "Pat chicken dry before cooking for better browning and crispy skin",
            "Brine chicken for 30 minutes to 2 hours for juicier meat",
            "Use a meat thermometer - chicken is done at 165°F (74°C) internal temperature",
            "Let chicken rest for 5-10 minutes after cooking before cutting",
            "Pound chicken breasts to even thickness for uniform cooking",
        ],
        "vegetables": [
            "Don't overcrowd the pan when roasting - vegetables need space to caramelize",
            "Salt vegetables after cooking, not before, to prevent them from releasing water",
            "Blanch green vegetables in salted water, then shock in ice water to keep color bright",
            "Cut vegetables uniformly for even cooking",
            "Save vegetable scraps to make homemade vegetable stock",
        ],
        "seasoning": [
            "Season in layers throughout cooking, not just at the end",
            "Taste as you go and adjust seasoning accordingly",
            "Add salt to bring out flavors, acid (lemon/vinegar) to brighten them",
            "Toast whole spices before grinding for more intense flavor",
            "Add delicate herbs at the end, hardy herbs at the beginning",
        ],
        "knife skills": [
            "Keep knives sharp - a sharp knife is safer than a dull one",
            "Use a proper cutting board (wood or plastic, not glass)",
            "Curl your fingers when holding food to protect fingertips",
            "Rock the knife forward and back, don't saw",
            "Clean and dry knives immediately after use",
        ],
    }
    
    topic_lower = topic.lower()
    
    # Find matching topic
    matched_topic = None
    for key in tips_db:
        if key in topic_lower or topic_lower in key:
            matched_topic = key
            break
    
    if not matched_topic:
        available = ", ".join(tips_db.keys())
        return (f"Sorry, I don't have tips for '{topic}'. "
                f"Available topics: {available}")
    
    tips = tips_db[matched_topic]
    result = f"Cooking tips for {matched_topic.title()}:\n\n"
    
    for i, tip in enumerate(tips, 1):
        result += f"{i}. {tip}\n"
    
    return result


# ============================================================
# Main Agent Application
# ============================================================

async def main():
    """
    Main function to run the Cooking AI Agent.
    """
    print("=" * 70)
    print("🍳 Welcome to the Cooking AI Agent! 👨‍🍳")
    print("=" * 70)
    print("\nI'm your personal cooking assistant powered by AI!")
    print("I can help you with:")
    print("  • Finding recipes by cuisine and difficulty")
    print("  • Extracting ingredients for specific recipes")
    print("  • Providing cooking tips and techniques")
    print("\nType 'exit' or 'quit' to end the conversation.")
    print("=" * 70)
    print()
    
    # Get Azure OpenAI credentials from environment variable
    azure_api_key = os.getenv("AZURE_OPENAI_API_KEY")
    azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT")
    
    if not azure_api_key:
        print("❌ Error: AZURE_OPENAI_API_KEY not found in environment variables!")
        print("\nPlease set up your Azure OpenAI credentials:")
        print("1. Create a .env file in the project directory")
        print("2. Add: AZURE_OPENAI_API_KEY=your_api_key_here")
        print("3. Add: AZURE_OPENAI_ENDPOINT=your_endpoint_here")
        print("4. Add: AZURE_OPENAI_DEPLOYMENT=your_deployment_name")
        print("\nFor more information, see README.md")
        return
    
    # Initialize Azure OpenAI client
    openai_client = AsyncAzureOpenAI(
        api_key=azure_api_key,
        azure_endpoint=azure_endpoint,
        api_version="2024-08-01-preview",
    )
    
    # Create chat client for the agent
    chat_client = OpenAIChatClient(
        async_client=openai_client,
        model_id=deployment_name,  # Azure OpenAI deployment name
    )
    
    # Create the cooking agent with tools
    agent = ChatAgent(
        chat_client=chat_client,
        name="CookingAssistant",
        instructions=(
            "You are a friendly and knowledgeable cooking assistant. "
            "Help users find recipes, understand ingredients, and learn cooking techniques. "
            "When users ask about recipes, use the search_recipes tool to find appropriate suggestions. "
            "When they want to know ingredients for a specific dish, use the extract_ingredients tool. "
            "For cooking advice and tips, use the get_cooking_tips tool. "
            "Be encouraging and make cooking seem approachable and fun! "
            "If a user's question is unclear, ask clarifying questions. "
            "Always provide helpful context and suggestions."
        ),
        tools=[search_recipes, extract_ingredients, get_cooking_tips],
    )
    
    # Create a conversation thread for context persistence
    thread = agent.get_new_thread()
    
    print("✅ Cooking Agent is ready! Start chatting below:\n")
    
    # Interactive conversation loop
    while True:
        try:
            # Get user input
            user_input = input("You: ").strip()
            
            if not user_input:
                continue
            
            # Check for exit commands
            if user_input.lower() in ['exit', 'quit', 'bye', 'goodbye']:
                print("\n👋 Thanks for using the Cooking AI Agent! Happy cooking!")
                break
            
            # Process user input with the agent
            print("Assistant: ", end="", flush=True)
            result = await agent.run(user_input, thread=thread)
            print(result.text)
            print()
            
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye! Happy cooking!")
            break
        except Exception as e:
            print(f"\n❌ An error occurred: {e}")
            print("Please try again.\n")


if __name__ == "__main__":
    asyncio.run(main())

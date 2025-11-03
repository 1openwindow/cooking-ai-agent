import { ActivityTypes } from "@microsoft/agents-activity";
import { AgentApplication, MemoryStorage, TurnContext } from "@microsoft/agents-hosting";
import { AzureOpenAI, OpenAI } from "openai";
import config from "./config";

const client = new AzureOpenAI({
  apiVersion: "2024-12-01-preview",
  apiKey: config.azureOpenAIKey,
  endpoint: config.azureOpenAIEndpoint,
  deployment: config.azureOpenAIDeploymentName,
});

const systemPrompt = `You are a friendly and knowledgeable cooking assistant AI agent. 
Help users find recipes, understand ingredients, and learn cooking techniques. 
When users ask about recipes, search for appropriate suggestions based on cuisine and difficulty. 
When they want to know ingredients for a specific dish, provide detailed ingredient lists. 
For cooking advice and tips, share helpful cooking techniques. 
Be encouraging and make cooking seem approachable and fun! 
If a user's question is unclear, ask clarifying questions. 
Always provide helpful context and suggestions.

You have access to the following capabilities:
1. Search for recipes by cuisine type (Italian, Chinese, Mexican, Indian) and difficulty (easy, medium, hard)
2. Extract ingredients for specific recipes with measurements and cooking times
3. Provide cooking tips for topics like pasta, rice, chicken, vegetables, seasoning, and knife skills

Examples of what you can help with:
- "Find me easy Italian recipes"
- "What ingredients do I need for Kung Pao Chicken?"
- "Give me cooking tips for pasta"
- "Show me medium difficulty Mexican dishes"`;

// ============================================================
// Tool Functions - Recipe Search and Ingredient Extraction
// ============================================================

function searchRecipes(cuisine: string, difficulty: string = "medium"): string {
  // Mock recipe database - in production, this would call a real recipe API
  const recipes: Record<string, Record<string, string[]>> = {
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
  };

  const cuisineLower = cuisine.toLowerCase();
  const difficultyLower = difficulty.toLowerCase();

  if (!(cuisineLower in recipes)) {
    const available = Object.keys(recipes).join(", ");
    return `Sorry, I don't have recipes for ${cuisine} cuisine. Available cuisines: ${available}`;
  }

  if (!(difficultyLower in recipes[cuisineLower])) {
    return `Invalid difficulty level. Please choose: easy, medium, or hard`;
  }

  const recipeList = recipes[cuisineLower][difficultyLower];
  let result = `Here are ${difficulty} ${cuisine} recipes:\n\n`;
  recipeList.forEach((recipe, index) => {
    result += `${index + 1}. ${recipe}\n`;
  });

  return result;
}

function extractIngredients(recipeName: string): string {
  interface RecipeData {
    ingredients: string[];
    servings: string;
    prep_time: string;
    cook_time: string;
  }

  // Mock ingredient database - in production, this would query a recipe database
  const ingredientsDb: Record<string, RecipeData> = {
    "spaghetti aglio e olio": {
      ingredients: [
        "400g spaghetti pasta",
        "6 cloves garlic, thinly sliced",
        "1/2 cup extra virgin olive oil",
        "1 teaspoon red pepper flakes",
        "1/4 cup fresh parsley, chopped",
        "Salt to taste",
        "Freshly ground black pepper",
        "Parmesan cheese (optional, for serving)",
      ],
      servings: "4 people",
      prep_time: "5 minutes",
      cook_time: "15 minutes",
    },
    "kung pao chicken": {
      ingredients: [
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
      servings: "4 people",
      prep_time: "15 minutes",
      cook_time: "20 minutes",
    },
    "butter chicken": {
      ingredients: [
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
      servings: "6 people",
      prep_time: "20 minutes (plus marinating time)",
      cook_time: "30 minutes",
    },
    "chicken enchiladas": {
      ingredients: [
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
      servings: "4-6 people",
      prep_time: "20 minutes",
      cook_time: "25 minutes",
    },
    "caprese salad": {
      ingredients: [
        "4 large ripe tomatoes, sliced",
        "400g fresh mozzarella cheese, sliced",
        "Fresh basil leaves",
        "1/4 cup extra virgin olive oil",
        "2 tablespoons balsamic vinegar or glaze",
        "Sea salt flakes",
        "Freshly ground black pepper",
      ],
      servings: "4 people",
      prep_time: "10 minutes",
      cook_time: "0 minutes",
    },
  };

  const recipeLower = recipeName.toLowerCase();

  // Try to find a matching recipe
  let matchedRecipe: string | null = null;
  for (const key in ingredientsDb) {
    if (key.includes(recipeLower) || recipeLower.includes(key)) {
      matchedRecipe = key;
      break;
    }
  }

  if (!matchedRecipe) {
    return `Sorry, I don't have ingredient information for '${recipeName}'. ` +
      `Try asking about specific recipes like 'Spaghetti Aglio e Olio', ` +
      `'Kung Pao Chicken', 'Butter Chicken', 'Chicken Enchiladas', or 'Caprese Salad'.`;
  }

  const recipeData = ingredientsDb[matchedRecipe];
  let result = `Ingredients for ${matchedRecipe.replace(/\b\w/g, l => l.toUpperCase())}:\n\n`;
  result += `Servings: ${recipeData.servings}\n`;
  result += `Prep Time: ${recipeData.prep_time}\n`;
  result += `Cook Time: ${recipeData.cook_time}\n\n`;
  result += "Ingredients:\n";

  recipeData.ingredients.forEach(ingredient => {
    result += `• ${ingredient}\n`;
  });

  return result;
}

function getCookingTips(topic: string): string {
  const tipsDb: Record<string, string[]> = {
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
  };

  const topicLower = topic.toLowerCase();

  // Find matching topic
  let matchedTopic: string | null = null;
  for (const key in tipsDb) {
    if (key.includes(topicLower) || topicLower.includes(key)) {
      matchedTopic = key;
      break;
    }
  }

  if (!matchedTopic) {
    const available = Object.keys(tipsDb).join(", ");
    return `Sorry, I don't have tips for '${topic}'. Available topics: ${available}`;
  }

  const tips = tipsDb[matchedTopic];
  let result = `Cooking tips for ${matchedTopic.replace(/\b\w/g, l => l.toUpperCase())}:\n\n`;

  tips.forEach((tip, index) => {
    result += `${index + 1}. ${tip}\n`;
  });

  return result;
}

// Helper function to determine what the user is asking for and call appropriate function
function processUserRequest(userMessage: string): string {
  const messageLower = userMessage.toLowerCase();
  
  // Check for recipe search requests
  if (messageLower.includes("recipe") || messageLower.includes("find") || messageLower.includes("show me") || messageLower.includes("suggest")) {
    // Extract cuisine and difficulty
    const cuisines = ["italian", "chinese", "mexican", "indian"];
    const difficulties = ["easy", "medium", "hard"];
    
    let cuisine = "";
    let difficulty = "medium"; // default
    
    for (const c of cuisines) {
      if (messageLower.includes(c)) {
        cuisine = c;
        break;
      }
    }
    
    for (const d of difficulties) {
      if (messageLower.includes(d)) {
        difficulty = d;
        break;
      }
    }
    
    if (cuisine) {
      return searchRecipes(cuisine, difficulty);
    }
  }
  
  // Check for ingredient requests
  if (messageLower.includes("ingredient") || messageLower.includes("what do i need") || messageLower.includes("shopping list")) {
    // Try to extract recipe name from common patterns
    const patterns = [
      /ingredients? for (.+?)(?:\?|$)/i,
      /what (?:do )?i need (?:for|to make) (.+?)(?:\?|$)/i,
      /(.+?) ingredients?/i,
    ];
    
    for (const pattern of patterns) {
      const match = userMessage.match(pattern);
      if (match && match[1]) {
        return extractIngredients(match[1].trim());
      }
    }
  }
  
  // Check for cooking tips requests
  if (messageLower.includes("tip") || messageLower.includes("advice") || messageLower.includes("how to")) {
    const topics = ["pasta", "rice", "chicken", "vegetables", "seasoning", "knife skills"];
    
    for (const topic of topics) {
      if (messageLower.includes(topic)) {
        return getCookingTips(topic);
      }
    }
  }
  
  return ""; // Return empty string to let AI handle the general response
}

// Define storage and application
const storage = new MemoryStorage();
export const agentApp = new AgentApplication({
  storage,
});

agentApp.onConversationUpdate("membersAdded", async (context: TurnContext) => {
  await context.sendActivity(
    `🍳 Hi there! I'm your personal Cooking AI Assistant! 👨‍🍳\n\n` +
    `I can help you with:\n` +
    `• Finding recipes by cuisine and difficulty\n` +
    `• Extracting ingredients for specific recipes\n` +
    `• Providing cooking tips and techniques\n\n` +
    `Try asking me something like:\n` +
    `- "Find me easy Italian recipes"\n` +
    `- "What ingredients do I need for Kung Pao Chicken?"\n` +
    `- "Give me cooking tips for pasta"\n\n` +
    `What would you like to cook today?`
  );
});

// Listen for ANY message to be received. MUST BE AFTER ANY OTHER MESSAGE HANDLERS
agentApp.onActivity(ActivityTypes.Message, async (context: TurnContext) => {
  const userMessage = context.activity.text;
  
  // First, try to process the request with our cooking functions
  const functionResult = processUserRequest(userMessage);
  
  if (functionResult) {
    // If we have a direct function result, send it
    await context.sendActivity(functionResult);
  } else {
    // Otherwise, use AI to generate a response with cooking context
    const result = await client.chat.completions.create({
      messages: [
        {
          role: "system",
          content: systemPrompt,
        },
        {
          role: "user",
          content: userMessage,
        },
      ],
      model: "",
    });
    
    let answer = "";
    for (const choice of result.choices) {
      answer += choice.message.content;
    }
    await context.sendActivity(answer);
  }
});

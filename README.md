# 🍳 Cooking AI Agent

An intelligent cooking assistant powered by **GitHub Models** and **Microsoft Agent Framework** that helps you discover recipes, extract ingredients, and learn cooking techniques through natural conversation.

## ✨ Features

- 🔍 **Recipe Search**: Find recipes by cuisine type (Italian, Chinese, Mexican, Indian) and difficulty level
- 📝 **Ingredient Extraction**: Get detailed ingredient lists with measurements for specific recipes
- 💡 **Cooking Tips**: Learn professional cooking techniques and tips
- 💬 **Interactive Console**: Natural conversation interface with context awareness
- 🤖 **AI-Powered**: Leverages GPT-4.1-mini model for intelligent responses

## 🏗️ Architecture

This application uses:
- **Microsoft Agent Framework** (Python): A flexible framework for building AI agents with tool calling capabilities
- **Azure OpenAI Service**: Enterprise-grade AI models with enhanced security and reliability
- **OpenAI SDK**: For model interaction via Azure's OpenAI-compatible API

### Why These Choices?

- **Azure OpenAI Service**: Enterprise-grade security, reliability, and compliance with Azure's infrastructure
- **Agent Framework**: Built specifically for agent development with native tool calling, multi-turn conversations, and extensible architecture
- **GPT-4.1**: Advanced reasoning capabilities for intelligent conversational AI

## 📋 Prerequisites

- Python 3.9 or higher
- GitHub account (for GitHub Personal Access Token)

## 🚀 Getting Started

### 1. Clone or Download This Project

```bash
cd new-aitk-agent_1030
```

### 2. Set Up Python Environment (Recommended)

Create and activate a virtual environment:

**Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**macOS/Linux:**
```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

⚠️ **IMPORTANT**: The `--pre` flag is required while Agent Framework is in preview.

```bash
pip install --pre -r requirements.txt
```

This will install:
- `agent-framework-azure-ai` (includes Azure AI/OpenAI support, workflows, and orchestrations)
- `python-dotenv` (for environment variable management)

### 4. Get Your Azure OpenAI Credentials

You'll need access to Azure OpenAI Service. If you already have credentials:
- **API Key**: Your Azure OpenAI API key
- **Endpoint**: Your Azure OpenAI endpoint URL (e.g., `https://your-resource.openai.azure.com/`)
- **Deployment Name**: Your model deployment name (e.g., `gpt-4.1`)

If you don't have Azure OpenAI access, you can request it at the [Azure Portal](https://portal.azure.com).

### 5. Configure Environment Variables

Create a `.env` file in the project directory:

```bash
# Copy the example file
cp .env.example .env
```

Edit `.env` and add your Azure OpenAI credentials:

```
AZURE_OPENAI_API_KEY=your_api_key_here
AZURE_OPENAI_ENDPOINT=https://your-resource-name.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT=gpt-4.1
```

**Security Note**: Never commit your `.env` file to version control. It's already included in `.gitignore`.

### 6. Run the Application

```bash
python cooking_agent.py
```

## 💬 Usage Examples

Once the agent is running, you can interact with it naturally. Here are some examples:

### Recipe Search

```
You: I want to make something Italian but I'm a beginner
Assistant: [Uses search_recipes tool to find easy Italian recipes]

You: Show me medium difficulty Chinese recipes
Assistant: [Provides Chinese recipes at medium difficulty]
```

### Ingredient Extraction

```
You: What ingredients do I need for Kung Pao Chicken?
Assistant: [Uses extract_ingredients tool to list all ingredients with measurements]

You: Can you tell me what's in Butter Chicken?
Assistant: [Provides detailed ingredient list for Butter Chicken]
```

### Cooking Tips

```
You: How do I cook perfect pasta?
Assistant: [Uses get_cooking_tips tool to provide pasta cooking tips]

You: Give me tips for preparing chicken
Assistant: [Shares chicken preparation and cooking techniques]
```

### Multi-Turn Conversations

The agent maintains context across the conversation:

```
You: I want to cook something Chinese
Assistant: What difficulty level would you prefer? Easy, medium, or hard?

You: Medium please
Assistant: [Shows medium difficulty Chinese recipes]

You: Tell me more about the first one
Assistant: [Provides ingredients for the first recipe mentioned]
```

## 🛠️ Project Structure

```
new-aitk-agent_1030/
├── cooking_agent.py      # Main application with agent and tools
├── requirements.txt      # Python dependencies
├── .env.example         # Example environment variables
├── .env                 # Your actual environment variables (not in git)
└── README.md           # This file
```

## 🎯 Available Tools

The agent has access to three specialized tools:

1. **`search_recipes`**: Searches for recipes based on:
   - Cuisine type: Italian, Chinese, Mexican, Indian
   - Difficulty: easy, medium, hard
   
2. **`extract_ingredients`**: Extracts ingredient lists for:
   - Spaghetti Aglio e Olio
   - Kung Pao Chicken
   - Butter Chicken
   - Chicken Enchiladas
   - Caprese Salad
   - And more (easily extensible)

3. **`get_cooking_tips`**: Provides tips for:
   - Pasta cooking
   - Rice preparation
   - Chicken cooking
   - Vegetable preparation
   - Seasoning techniques
   - Knife skills

## 🔧 Customization

### Adding More Recipes

Edit `cooking_agent.py` and add to the `recipes` dictionary in the `search_recipes` function:

```python
recipes = {
    "your_cuisine": {
        "easy": ["Recipe 1", "Recipe 2"],
        "medium": ["Recipe 3"],
        "hard": ["Recipe 4"],
    }
}
```

### Adding More Ingredients

Add to the `ingredients_db` dictionary in the `extract_ingredients` function:

```python
ingredients_db = {
    "your recipe name": {
        "ingredients": ["ingredient 1", "ingredient 2"],
        "servings": "4 people",
        "prep_time": "15 minutes",
        "cook_time": "30 minutes",
    }
}
```

### Changing the AI Model

In `cooking_agent.py`, modify the `model_id` parameter:

```python
chat_client = OpenAIChatClient(
    async_client=openai_client,
    model_id="openai/gpt-5-mini",  # or any other GitHub model
)
```

Available GitHub models include:
- `openai/gpt-4.1-mini` (recommended - balanced performance)
- `openai/gpt-4.1-nano` (fastest, most cost-effective)
- `openai/gpt-4.1` (highest quality)
- `openai/gpt-5-mini` (latest, excellent performance)
- And many more!

## 📚 Learn More

### Microsoft Agent Framework
- [GitHub Repository](https://github.com/microsoft/agent-framework)
- Documentation for MCP, multimodal, Assistants API, multi-agent workflows

### GitHub Models
- [GitHub Models Documentation](https://docs.github.com/en/github-models)
- Free-tier access for development and experimentation
- Easy model switching with a single endpoint

### Azure AI Foundry (For Production)
For production deployments or more complex workflows, consider Azure AI Foundry:
- Dedicated model deployments
- Enhanced security and compliance
- Multi-agent orchestration
- Production-grade scaling

## 🐛 Troubleshooting

### Import Errors

If you see import errors for `agent_framework` or `openai`:
```bash
pip install --pre -r requirements.txt
```

Make sure you include the `--pre` flag!

### GitHub Token Issues

If you get authentication errors:
1. Verify your `.env` file exists and contains `GITHUB_TOKEN=your_token`
2. Check that your token is valid (not expired)
3. Ensure no extra spaces or quotes around the token

### Rate Limits

GitHub Models has rate limits on the free tier. If you hit them:
- Wait a few minutes and try again
- Consider upgrading to a paid plan
- Or deploy your own model on Azure AI Foundry

## 🤝 Contributing

Feel free to extend this agent with:
- More cuisines and recipes
- Integration with real recipe APIs (Spoonacular, Edamam, etc.)
- Meal planning features
- Nutrition information
- Shopping list generation
- Voice input/output
- Web or mobile interface

## 📄 License

This project is provided as-is for educational and development purposes.

## 🙏 Acknowledgments

- Built with [Microsoft Agent Framework](https://github.com/microsoft/agent-framework)
- Powered by [GitHub Models](https://github.com/marketplace/models)
- AI models provided by OpenAI via GitHub

---

**Happy Cooking! 🍳👨‍🍳👩‍🍳**

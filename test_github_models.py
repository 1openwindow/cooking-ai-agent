"""
Test script to verify GitHub Models access
"""
import os
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv

load_dotenv()

endpoint = "https://models.github.ai/inference"
model = "gpt-4o-mini"
token = os.environ.get("GITHUB_TOKEN")

if not token:
    print("❌ GITHUB_TOKEN not found in environment")
    exit(1)

print(f"Testing GitHub Models with endpoint: {endpoint}")
print(f"Model: {model}")
print(f"Token (first 10 chars): {token[:10]}...")

try:
    client = ChatCompletionsClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(token),
    )

    response = client.complete(
        messages=[
            SystemMessage("You are a helpful assistant."),
            UserMessage("Say 'Hello World' if you can hear me."),
        ],
        model=model
    )

    print("\n✅ Success!")
    print(f"Response: {response.choices[0].message.content}")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    print("\nPossible issues:")
    print("1. Your GitHub token may not have 'models:read' permission")
    print("2. Go to https://github.com/settings/tokens")
    print("3. Create a new token (classic) with 'models:read' scope checked")
    print("4. Update your .env file with the new token")

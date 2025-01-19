import openai
import json
import sys

# Load API key from config.json
try:
    with open("config.json") as config_file:
        config = json.load(config_file)
        openai.api_key = config["api_key"]
except FileNotFoundError:
    print("Error: config.json not found. Please create one with your API key.")
    sys.exit(1)
except KeyError:
    print("Error: API key not found in config.json.")
    sys.exit(1)

def chat_with_gpt(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        return f"An error occurred: {e}"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 chatgpt_cli.py '<your question>'")
        sys.exit(1)

    user_prompt = " ".join(sys.argv[1:])
    print(chat_with_gpt(user_prompt))

import openai
import json
import sys
import subprocess

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

def get_last_bash_command():
    try:
        # Fetch the last command from bash history
        last_command = subprocess.check_output(['tail', '-n', '1', '~/.bash_history'], text=True).strip()
        return last_command
    except Exception as e:
        return f"Error retrieving last command: {e}"

def chat_with_gpt(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"An error occurred: {str(e)}"

if __name__ == "__main__":
    if len(sys.argv) == 1:  # No command provided, analyze the last bash command
        print("Analyzing the last command from bash...")
        last_command = get_last_bash_command()
        if "Error" in last_command:
            print(last_command)
        else:
            print(f"Last command: {last_command}")
            prompt = f"The following bash command was run, and it might have caused an issue: `{last_command}`. Can you help debug it?"
            print(chat_with_gpt(prompt))
    else:
        user_prompt = " ".join(sys.argv[1:])
        print(chat_with_gpt(user_prompt))

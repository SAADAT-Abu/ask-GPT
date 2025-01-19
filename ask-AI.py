import sys
import json
import subprocess
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

CONFIG_FILE = "config.json"
DEFAULT_MODEL = "gpt2"  # Default Hugging Face model

def load_config():
    """Load the configuration from config.json or return an empty dictionary."""
    try:
        with open(CONFIG_FILE, "r") as config_file:
            return json.load(config_file)
    except FileNotFoundError:
        print(f"Error: {CONFIG_FILE} not found. Creating a new configuration file.")
        return {}
    except json.JSONDecodeError:
        print(f"Error: Malformed {CONFIG_FILE}. Resetting configuration.")
        return {}

def save_config(config):
    """Save the configuration to config.json."""
    with open(CONFIG_FILE, "w") as config_file:
        json.dump(config, config_file, indent=4)

def get_preferred_model(config):
    """Retrieve the preferred Hugging Face model or use the default."""
    if "huggingface_model" in config:
        return config["huggingface_model"]
    else:
        print(f"No preferred Hugging Face model found. Using default: {DEFAULT_MODEL}")
        config["huggingface_model"] = DEFAULT_MODEL
        save_config(config)
        return DEFAULT_MODEL

def get_last_command():
    """Fetch the last command from the bash history."""
    try:
        last_command = subprocess.check_output(['tail', '-n', '1', '~/.bash_history'], text=True).strip()
        return last_command
    except Exception as e:
        return f"Error retrieving last command: {e}"

def chat_with_huggingface(prompt, model_name):
    """
    Generate a response using Hugging Face's transformers.
    :param prompt: The input prompt for the model.
    :param model_name: The name of the Hugging Face model to use.
    :return: The generated response as a string.
    """
    try:
        # Load the model and tokenizer
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForCausalLM.from_pretrained(model_name)
        hf_pipeline = pipeline("text-generation", model=model, tokenizer=tokenizer)

        # Generate a response
        response = hf_pipeline(prompt, max_length=100, num_return_sequences=1)
        return response[0]["generated_text"]
    except Exception as e:
        return f"An error occurred with Hugging Face: {e}"

if __name__ == "__main__":
    if len(sys.argv) == 1:  # No arguments provided, fetch the last command
        print("Analyzing the last terminal command...")
        last_command = get_last_command()
        if "Error" in last_command:
            print(last_command)
        else:
            print(f"Last command: {last_command}")
            config = load_config()
            preferred_model = get_preferred_model(config)
            prompt = f"The following terminal command was run: `{last_command}`. Can you analyze it or debug potential errors?"
            print(chat_with_huggingface(prompt, preferred_model))
    elif len(sys.argv) == 2 and sys.argv[1] == "help":
        print("Usage:")
        print("  python3 ask-AI.py               # Analyze the last terminal command")
        print("  python3 ask-AI.py <your query>  # Ask a question")
    else:
        # User provided a query
        config = load_config()
        preferred_model = get_preferred_model(config)
        user_prompt = " ".join(sys.argv[1:])
        print(chat_with_huggingface(user_prompt, preferred_model))


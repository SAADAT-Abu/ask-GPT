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

from transformers import AutoModelForCausalLM, AutoModelForSeq2SeqLM, AutoTokenizer, pipeline

def chat_with_huggingface(prompt, model_name):
    """
    Generate a response using Hugging Face's transformers.
    Automatically handles causal and encoder-decoder models.
    :param prompt: The input prompt for the model.
    :param model_name: The name of the Hugging Face model to use.
    :return: The generated response as a string.
    """
    try:
        # Load the tokenizer
        tokenizer = AutoTokenizer.from_pretrained(model_name)

        # Determine the model type (causal or encoder-decoder)
        if "t5" in model_name or "bart" in model_name or "mbart" in model_name:
            model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
            hf_pipeline = pipeline("text2text-generation", model=model, tokenizer=tokenizer)
        else:
            model = AutoModelForCausalLM.from_pretrained(model_name)
            hf_pipeline = pipeline("text-generation", model=model, tokenizer=tokenizer)

        # Generate a response
        response = hf_pipeline(
            prompt,
            max_length=50,  # Limit response length
            temperature=0.5,  # Reduce randomness
            top_k=50,  # Limit token diversity
            top_p=0.9,  # Nucleus sampling
            do_sample=True,  # Enable sampling
            num_return_sequences=1,
            truncation=True,
            pad_token_id=tokenizer.eos_token_id
        )
        return response[0]["generated_text"]
    except Exception as e:
        return f"An error occurred with Hugging Face: {e}"

def clean_response(response_text):
    """Remove repetitive phrases and trim output."""
    sentences = response_text.split('. ')
    unique_sentences = list(dict.fromkeys(sentences))  # Remove duplicates
    return '. '.join(unique_sentences[:2]) + '.'  # Limit to 2 sentences

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

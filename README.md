# Ask-GPT

A versatile command-line tool that allows you to interact with AI models, analyze terminal commands, and debug errors. It can use OpenAI API or Hugging Face models to provides a seamless, user-friendly experience for both querying and troubleshooting.

## Features

1. **Ask Questions**: Use Hugging Face models to answer questions and perform natural language tasks.
2. **Analyze Terminal Commands**: Automatically fetch and debug the last executed terminal command.
3. **Preferred Model Configuration**: Saves your preferred Hugging Face model in a shared configuration file (`config.json`) for future use.
4. **Error Handling**: Provides meaningful responses to terminal issues and other queries.
5. **Customizable**: Easily switch models and configurations as per your needs.

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/SAADAT-Abu/ask-GPT.git
   cd ask-GPT
   ```

2. Install requirements
   ```bash
   pip install -r requirements.txt
   ```
   
3. Configure the Tool

   Create a config.json file in the project root.
   Add your API key in the following format:

  ```bash
  {
    "api_key": "YOUR_OPENAI_API_KEY",
    "huggingface_model": "google/flan-t5-small"
  }
  ```
api_key: Your OpenAI API key (if needed for other tools in the package).
huggingface_model: Your preferred Hugging Face model (e.g., gpt2, bloom, flan-t5).

## 4. Usage 

   ```bash
   python3 ask-GPT.py "Your question here"

  ```

Example output:

  ```bash
   Analyzing the last terminal command...
   Last command: ls -l /nonexistentpath
   Response: The command tries to list files in a non-existent directory. Check the path for typos or ensure the directory exists.
  ```
Ask a Question

  ```bash
   python3 ask-AI.py "What is the capital of France?"
  ```
Help

  ```bash
   python3 ask-AI.py help
  ```

## 5. Optional Enhancements

   Add an Alias: Add this to your shell configuration file (e.g., ~/.bashrc or ~/.zshrc):

  ```bash

   alias ask-GPT="python3 /path/to/ask-GPT.py"
   alias ask-AI="python3 /path/to/ask-AI.py"

   source ~/.bashrc  # or source ~/.zshrc

  ```

## Supported Hugging Face Models
The tool supports various Hugging Face models. Specify your preferred model in config.json. Examples include:

1. **gpt2:** A lightweight and fast model for text generation.
2. **bloom:** A multilingual large language model.
3. **flan-t5:** Google's instruction-tuned language model.
To change the model, update the huggingface_model key in config.json or delete the file to reset.



## Contributing:

Feel free to fork and submit pull requests for enhancements!



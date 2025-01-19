# ChatGPT CLI

A simple command-line tool to interact with OpenAI's ChatGPT from any terminal.

## Features
- Query ChatGPT directly from the terminal.
- Uses OpenAI's GPT-4 (or GPT-3.5 if specified).
- Simple setup and usage.

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/chatgpt-cli.git
   cd chatgpt-cli
   ```

2. Install requirements
   ```bash
   pip install -r requirements.txt
   ```
3. Add your OpenAI API key:

   Create a config.json file in the project root.
   Add your API key in the following format:

```
  {
    "api_key": "YOUR_API_KEY"
  }
```

4. Usage 

```bash
   python3 chatgpt_cli.py "Your question here"
```

5. Optional Enhancements

   Add an Alias: Add this to your shell configuration file (e.g., ~/.bashrc or ~/.zshrc):

```bash

alias chatgpt="python3 /path/to/chatgpt_cli.py"

chatgpt "Explain quantum entanglement."

```

Contributing:

Feel free to fork and submit pull requests for enhancements!



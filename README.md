# Overview

This project is meant to be a starting point for PR (Press Releases, derived from news articles) summarization using the [latest OpenAI model of generative AI](https://platform.openai.com/docs/models/gpt-4)

## Project Contents

This project contains the following files and folders:
 `.streamlit`: This folder contains the 'secrets.toml' file, holding an API key for OpenAI.
- `engine`: This folder contains the various 'engine' modules, which host wrappers for interacting with the OpenAI API.
- `main.py`: This file contains the main logic and entry point of the Streamlit app.
- `requirements.txt`: This file contains the list of Python packages that your project depends on.

## Prerequisites

- Python 3.12 (CAN'T run on a higher python version due to compatibility issues with 'llama-index' package. Can run on a lower python version (but not tested)
- Create a directory under root named `.streamlit` and one file: `secrets.toml`. File should contain two variables keys in the following format:
  - `OPENAI_KEY="<key_you_get_from_openai>"`
  - `OPENAI_API_KEY="<key_you_get_from_openai>"`
  - you get the keys at https://platform.openai.com/account/api-keys
- First time execution can take a bit to load Tensorflow universal-sentence-encoder model. Subsequent executions will be faster.

## Installations

- `pip install -r requirements.txt`

## Run the app

- `streamlit run main.py` from root project folder in terminal. **App is updated automatically on code change!**
-  Login with credentials provided by data-infra@seekingalpha.com team. ** Please note, that credentials are auto saved on machine, and there is no need to re-login each and every time.

## Run in Docker container

- `docker build -t openai-pr-summarization .` from root project folder in terminal.
- `docker run -p 8501:8501 openai-pr-summarization:latest` from root project folder in terminal.
- Access UI by browsing to: http://localhost:8501/

## Usage

- `Number of bullet points` - the number of bullet points to sum the text into
- `Prefix text before input text` - pre-defined prefix text to go before the actual input text (can be edited) 
- `Input text` - the actual input text
- `Token count` - automatic GPT token calculation (can't be edited, can be used to estimate pricing of the query)
- `Engine Type` - selection of desired GPT engine (GPT4 is the default)
- `temperature` - control of the 'risk' element of the engine, the higher, the riskier (more experimental) will be the results
- `max_output_tokens` - control the maximum output (result) tokens 
- `Generate summary` - Generates response from the engine
- `Summarized text` - Shows generated response from the engine (depends on the button-click from above, can't be edited)
- `Calculate similarity` - Calculating similarity between 'Input text' and 'Summarized text' (using tensorflow TfHubUniversalSentenceEncoder)

## Install as a separate library

It's possible to install the engine as a separate library (module):

- Run `pip install git+ssh://git@github.com/seekingalpha/openai-pr-summarization.git` from local python environment (must be Python 3.8 or higher). A pre-configured SSH key is required.
- Import the desired module, e.g. gpt `from openai_wrapper_functions.gpt import GPTEngine`
- Get existing environment variables (please check with devops team for the proper way to integrate new env variables into your execution environment. In case of AF2, the best way would be to store them in airflow var and fetch from there) for OPENAI, i.e.: `os.environ.get('OPENAI_KEY')` & `os.environ.get('OPENAI_API_KEY')`. In case you don't have any, please generate one at: https://platform.openai.com/account/api-keys
- Use simply by calling a static function. e.g. `GPTEngine.summarize(prefix='generate a summary', prompt='some input text', temperature=0.3, max_tokens=256)`
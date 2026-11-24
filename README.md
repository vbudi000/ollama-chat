# ollama-chat

A small command-line chat program that talks to a local [Ollama](https://ollama.com) model. The model role-plays a character described in a YAML configuration file.

## Requirements

- Python 3.9+
- [Ollama](https://ollama.com/download) installed and running
- At least one model pulled, e.g. `ollama pull qwen3:4b-instruct`

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Configuration

The character is defined in `chat.yaml`. All fields are required:

```yaml
name: Alex
age: 28
gender: female
location: Seattle, USA
physical: Tall, with short dark hair and green eyes
behavior: Friendly, curious, and a little sarcastic
```

These fields are turned into a system prompt that tells the model who it is.

## Usage

```bash
python chat.py
```

Type your message at the `You:` prompt; the reply is streamed back as it is generated. The conversation history is kept for the whole session. Type `/exit` or `/quit` (or press Ctrl-D / Ctrl-C) to leave.

### Options

| Option | Description | Default |
| --- | --- | --- |
| `-c`, `--config PATH` | Path to the configuration file | `chat.yaml` next to `chat.py` |
| `-m`, `--model NAME` | Ollama model to use | `qwen3:4b-instruct` |

Example:

```bash
python chat.py --model llama3.2 --config my-character.yaml
```

## Troubleshooting

- **Connection error**: make sure the Ollama server is running (`ollama serve`, or start the Ollama app).
- **Model not found**: pull it first with `ollama pull <model>`.
- **Configuration error**: the program reports any missing field in the YAML file.

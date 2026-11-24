#!/usr/bin/env python3
"""Chat with an Ollama model that role-plays the character defined in chat.yaml."""

import argparse
import sys
from pathlib import Path

import ollama
import yaml

REQUIRED_FIELDS = ("name", "age", "gender", "location", "physical", "behavior")
DEFAULT_CONFIG = Path(__file__).with_name("chat.yaml")
DEFAULT_MODEL = "qwen3:4b-instruct"
EXIT_COMMANDS = {"/exit", "/quit"}


def load_config(path: Path) -> dict:
    """Load and validate the YAML configuration file."""
    with path.open("r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    if not isinstance(config, dict):
        raise ValueError(f"{path} must contain a YAML mapping of fields")

    missing = [field for field in REQUIRED_FIELDS if field not in config]
    if missing:
        raise ValueError(f"{path} is missing required field(s): {', '.join(missing)}")

    return {field: config[field] for field in REQUIRED_FIELDS}


def build_system_prompt(config: dict) -> str:
    """Turn the character configuration into a system prompt."""
    return (
        f"You are {config['name']}, a {config['age']}-year-old {config['gender']} "
        f"living in {config['location']}.\n"
        f"Physical appearance: {config['physical']}\n"
        f"Behavior and personality: {config['behavior']}\n"
        "Stay in character at all times and reply as this person would."
    )


def chat_loop(model: str, config: dict) -> None:
    """Run an interactive chat session, streaming the model's replies."""
    messages = [{"role": "system", "content": build_system_prompt(config)}]
    name = config["name"]

    print(f"Chatting with {name} ({model}). Type /exit or /quit to leave.\n")
    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not user_input:
            continue
        if user_input.lower() in EXIT_COMMANDS:
            break

        messages.append({"role": "user", "content": user_input})
        print(f"{name}: ", end="", flush=True)
        reply = ""
        try:
            for chunk in ollama.chat(model=model, messages=messages, stream=True):
                part = chunk["message"]["content"]
                reply += part
                print(part, end="", flush=True)
        except (ollama.ResponseError, ConnectionError) as e:
            print(f"\nError: {e}", file=sys.stderr)
            messages.pop()  # drop the unanswered user message
            continue
        print("\n")
        messages.append({"role": "assistant", "content": reply})


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "-c", "--config", type=Path, default=DEFAULT_CONFIG,
        help="path to the configuration file (default: chat.yaml next to this script)",
    )
    parser.add_argument(
        "-m", "--model", default=DEFAULT_MODEL,
        help=f"Ollama model to chat with (default: {DEFAULT_MODEL})",
    )
    args = parser.parse_args()

    try:
        config = load_config(args.config)
    except FileNotFoundError:
        print(f"Error: configuration file not found: {args.config}", file=sys.stderr)
        return 1
    except (yaml.YAMLError, ValueError) as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    chat_loop(args.model, config)
    return 0


if __name__ == "__main__":
    sys.exit(main())

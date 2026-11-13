'''
IMPORTANT SETUP NOTES:
1. You will probably need to download dependencies via pip using the following commands:
- python -m pip install ddgs
- pip install llama-cpp-python --prefer-binary --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/cpu/
- python -m pip install fastapi uvicorn pydantic
2. Download a small quantized model in .gguf format and put it in a new folder at "%USERPROFILE%\Documents\Models".
3. Run this script for the first time. If it returns a command error, that is totally normal.
4. In cmd, run doskey miniolla=python C:\path\to\miniolla.py $* (replace with the actual path to this script
5. Do miniolla -h for the available commands... there's literally only three. To exit a chat, do Ctrl-C or /bye
'''
### 8KHomework © 2026 by IdiotsAndInnovation is licensed under CC BY-NC-SA 4.0. ###

import os
import re
import sys
import glob
import argparse
from llama_cpp import Llama
from ddgs import DDGS

MODELS_DIR = os.path.expandvars(r"%USERPROFILE%\Documents\Models")
# Ahemmmmmmmmmmmmmm... Don't mind how I instruct the LLM...
SYSTEM_PROMPT = """You are a helpful AI assistant with access to a live internet search tool.
Whenever the user asks about current events, recent news, real-time facts, or anything you are unsure about, you MUST use the search tool before answering.

To search the internet, output ONLY the following XML tag and nothing else:
<search>your concise search query</search>

Example:
User: research the effect of the iran war
Assistant: <search>effects of the 2026 Iran war</search>

Wait for the system to return the search results. Once you receive them, write a comprehensive, well-structured answer based on those results. Never make up search results."""
# Like I mean it's not the worst way?
def list_models():
    os.makedirs(MODELS_DIR, exist_ok=True)
    models = glob.glob(os.path.join(MODELS_DIR, "*.gguf"))
    if not models:
        print(f"No .gguf models found in {MODELS_DIR}")
        return
    print(f"{'NAME':<45} {'SIZE':<10}")
    print("-" * 55)
    for m in models:
        name = os.path.basename(m)
        size_gb = os.path.getsize(m) / (1024 ** 3)
        print(f"{name:<45} {size_gb:.2f} GB")

def resolve_model_path(model_query):
    if os.path.exists(model_query):
        return model_query
    os.makedirs(MODELS_DIR, exist_ok=True)
    models = glob.glob(os.path.join(MODELS_DIR, "*.gguf"))
    for m in models:
        if os.path.basename(m).lower() == model_query.lower():
            return m
    for m in models:
        if model_query.lower() in os.path.basename(m).lower():
            return m
    return None

def web_search(query, max_results=4):
    """Fetches live web results using ddgs."""
    print(f"\n[Tool Call -> Searching web for: '{query}']...")
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=max_results))
            if not results:
                return "No relevant web search results found."
            
            formatted = f"Search Results for '{query}':\n\n"
            for i, res in enumerate(results, 1):
                formatted += f"[{i}] Title: {res.get('title')}\nSource: {res.get('href')}\nSummary: {res.get('body')}\n\n"
            return formatted
    except Exception as e:
        return f"Web search error: {str(e)}"

def run_chat(model_query, n_ctx=4096, threads=None):
    model_path = resolve_model_path(model_query)
    if not model_path:
        print(f"Error: Could not find model matching '{model_query}' in {MODELS_DIR}")
        sys.exit(1)

    print(f"Loading {os.path.basename(model_path)} into RAM...")
    llm = Llama(
        model_path=model_path,
        n_ctx=n_ctx,
        n_gpu_layers=0,
        n_threads=threads,
        verbose=False
    )

    print("Model loaded successfully! Autonomous web search enabled.")
    print("Commands: /clear (reset history), /bye (exit)\n")

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    while True:
        try:
            user_input = input(">>> ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nExiting...")
            break

        if not user_input:
            continue

        if user_input.lower() in ["/bye", "/exit", "exit", "quit"]:
            break
        elif user_input.lower() == "/clear":
            messages = [{"role": "system", "content": SYSTEM_PROMPT}]
            print("Conversation context cleared.\n")
            continue

        messages.append({"role": "user", "content": user_input})

        # Agentic loop: handles model tool calls iteratively
        for _ in range(3):
            try:
                stream = llm.create_chat_completion(
                    messages=messages,
                    temperature=0.4,
                    stream=True
                )
                
                full_reply = ""
                buffer = ""
                is_tool_call = False

                for chunk in stream:
                    delta = chunk["choices"][0]["delta"]
                    if "content" in delta:
                        token = delta["content"]
                        full_reply += token
                        
                        # Buffer initial characters to detect <search> tool emission
                        if len(full_reply) < 15:
                            buffer += token
                            if "<search>" in full_reply:
                                is_tool_call = True
                        else:
                            if buffer:
                                if not is_tool_call:
                                    print(buffer, end="", flush=True)
                                buffer = ""
                            if not is_tool_call:
                                print(token, end="", flush=True)

                if buffer and not is_tool_call:
                    print(buffer, end="", flush=True)

                messages.append({"role": "assistant", "content": full_reply})

                # Check if the model triggered a search tag
                search_match = re.search(r"<search>(.*?)</search>", full_reply, re.DOTALL)
                if search_match:
                    query = search_match.group(1).strip()
                    search_results = web_search(query)
                    messages.append({
                        "role": "user",
                        "content": f"Tool Output:\n{search_results}\nNow answer my original request using these search results."
                    })
                    continue  # Loop back for the model to synthesize the final answer
                else:
                    print("\n")
                    break

            except KeyboardInterrupt:
                print("\n[Generation interrupted]\n")
                break
            except Exception as e:
                print(f"\n[Inference Error]: {e}\n")
                break

def main():
    parser = argparse.ArgumentParser(prog="miniolla")
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("list")
    run_parser = subparsers.add_parser("run")
    run_parser.add_argument("model")
    run_parser.add_argument("--ctx", type=int, default=4096)
    run_parser.add_argument("--threads", type=int, default=None)

    args = parser.parse_args()
    if args.command == "list":
        list_models()
    elif args.command == "run":
        run_chat(args.model, n_ctx=args.ctx, threads=args.threads)

if __name__ == "__main__":
    main()

import requests
import json
import sys

url = "http://18.199.190.33:8000/v1/chat/completions"

headers = {
    "Content-Type": "application/json",
}

def ask_question(question):
    payload = {
        "model": "TinyLlama/TinyLlama-1.1B-Chat-v1.0",
        "messages": [{"role": "user", "content": question}],
        "stream": True
    }

    response = requests.post(url, headers=headers, json=payload, stream=True)

    print("Bot:", end=" ", flush=True)
    for line in response.iter_lines():
        if line:
            line = line.decode('utf-8')
            if line.startswith("data: "):
                content = line[len("data: "):]
                if content.strip() == "[DONE]":
                    break
                try:
                    data = json.loads(content)
                    delta = data["choices"][0]["delta"]
                    if "content" in delta:
                        sys.stdout.write(delta["content"])
                        sys.stdout.flush()
                except json.JSONDecodeError:
                    continue
    print()  # new line after bot finishes

def main():
    print("Welcome to TinyLlama Chat! Type 'exit' to quit.\n")
    while True:
        question = input("You: ")
        if question.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break
        ask_question(question)

if __name__ == "__main__":
    main()

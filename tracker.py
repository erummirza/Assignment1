
import os
import json
import time
import requests
import re

from datetime import datetime, timezone
from dotenv import load_dotenv

load_dotenv(override=True)


# --------------------------------------------------
# 1. Configuration
# --------------------------------------------------

AssignmentPrompt = os.getenv(
    "TRACKER_PROMPT",
    "Explain how an AI Cost Tracker works. Describe API requests, input tokens, output tokens, response time, actual cost, estimated cost and error handling."
)

TIMEOUT_SECONDS = int(os.getenv("TIMEOUT_SECONDS", "180"))


# Illustrative paid-price estimates per 1 million tokens.
# Verify current provider pricing before using these figures.

PRICES = {
    "gemini": (
        float(os.getenv("GEMINI_INPUT_PRICE_PER_1M", "0.75")),
        float(os.getenv("GEMINI_OUTPUT_PRICE_PER_1M", "3.75"))
    ),
    "groq": (
        float(os.getenv("GROQ_INPUT_PRICE_PER_1M", "0.50")),
        float(os.getenv("GROQ_OUTPUT_PRICE_PER_1M", "1.50"))
    )
}


# --------------------------------------------------
# 2. Clean Markdown formatting
# --------------------------------------------------

def clean_markdown(text):
    # Remove bold Markdown markers (**text**)
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)

    return text


# --------------------------------------------------
# 3. Calculate API cost
# --------------------------------------------------

def calculate_cost(input_tokens, output_tokens, input_price, output_price):

    input_cost = input_tokens * input_price / 1_000_000

    output_cost = output_tokens * output_price / 1_000_000

    total_cost = input_cost + output_cost

    return total_cost


# --------------------------------------------------
# 4. Gemini API
# --------------------------------------------------

def call_gemini(prompt):

    api_key = os.getenv("GEMINI_API_KEY")

    model = os.getenv("GEMINI_MODEL", "gemini-4-hydrogen")

    if not api_key:
        raise ValueError("GEMINI_API_KEY is missing from .env")

    url = (
        f"https://generativelanguage.googleapis.com/v1beta/"
        f"models/{model}:generateContent"
    )

    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": api_key
    }

    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }

    response = requests.post(
        url,
        headers=headers,
        json=payload,
        timeout=TIMEOUT_SECONDS
    )

    response.raise_for_status()

    data = response.json()

    reply = data["candidates"][0]["content"]["parts"][0]["text"]

    usage = data.get("usageMetadata", {})

    return {
        "provider": "Gemini (free tier)",
        "model": model,
        "reply": clean_markdown(reply),
        "input_tokens": usage.get("promptTokenCount", 0),
        "output_tokens": usage.get("candidatesTokenCount", 0)
    }


# --------------------------------------------------
# 5. Groq API
# --------------------------------------------------

def call_groq(prompt):

    api_key = os.getenv("GROQ_API_KEY")

    model = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")

    if not api_key:
        raise ValueError("GROQ_API_KEY is missing from .env")

    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    payload = {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    }

    response = requests.post(
        url,
        headers=headers,
        json=payload,
        timeout=TIMEOUT_SECONDS
    )

    response.raise_for_status()

    data = response.json()

    usage = data.get("usage", {})

    reply = data["choices"][0]["message"]["content"]

    return {
        "provider": "Groq (free tier)",
        "model": model,
        "reply": clean_markdown(reply),
        "input_tokens": usage.get("prompt_tokens", 0),
        "output_tokens": usage.get("completion_tokens", 0)
    }


# --------------------------------------------------
# 6. Run one provider and calculate cost
# --------------------------------------------------

def run_one(provider_name, provider_function, prompt, free_tier=True):

    print("\n" + "=" * 60)

    print(f"Running {provider_name}...")

    start_time = time.time()

    try:

        result = provider_function(prompt)

        elapsed_time = time.time() - start_time

        input_tokens = result["input_tokens"]

        output_tokens = result["output_tokens"]

        input_price, output_price = PRICES[provider_name]

        estimated_cost = calculate_cost(
            input_tokens,
            output_tokens,
            input_price,
            output_price
        )

        actual_cost = 0.0 if free_tier else estimated_cost

        result["response_time_seconds"] = round(elapsed_time, 3)

        result["actual_cost_usd"] = actual_cost

        result["paid_price_equivalent_usd"] = estimated_cost

        result["status"] = "success"

        print("\nProvider:", result["provider"])

        print("Model:", result["model"])

        print("\nAI Response:\n")

        print(result["reply"])

        print("\nInput tokens:", input_tokens)

        print("Output tokens:", output_tokens)

        print("Speed:", round(elapsed_time, 3), "seconds")

        print("Actual cost: $", f"{actual_cost:.8f}")

        print(
            "Paid-price equivalent (estimated): $",
            f"{estimated_cost:.8f}"
        )

        return result

    except Exception as error:

        elapsed_time = time.time() - start_time

        error_result = {
            "provider": provider_name,
            "status": "error",
            "error": str(error),
            "response_time_seconds": round(elapsed_time, 3)
        }

        print(f"\n{provider_name} error:", error)

        return error_result


# --------------------------------------------------
# 7. Print comparison table
# --------------------------------------------------

def print_table(results):

    print("\n\n")

    print("=" * 90)

    print("GEMINI vs GROQ - SPEED AND COST")

    print("=" * 90)

    print(
        f"{'Provider':<22}"
        f"{'Status':<12}"
        f"{'Seconds':<12}"
        f"{'Tokens in/out':<18}"
        f"{'Actual Cost':<14}"
    )

    print("-" * 90)

    for result in results:

        provider = result.get("provider", "Unknown")

        status = result.get("status", "error")

        seconds = result.get("response_time_seconds", 0)

        input_tokens = result.get("input_tokens", 0)

        output_tokens = result.get("output_tokens", 0)

        actual_cost = result.get("actual_cost_usd", 0)

        print(
            f"{provider:<22}"
            f"{status:<12}"
            f"{seconds:<12}"
            f"{str(input_tokens) + '/' + str(output_tokens):<18}"
            f"${actual_cost:<13.8f}"
        )

    print("=" * 90)


# --------------------------------------------------
# 8. Main program
# --------------------------------------------------

def main():

    print("\nAI COST TRACKER - TRACK B")

    print("\nPrompt:", AssignmentPrompt)

    results = []

    # Both providers are currently configured as free-tier calls.
    results.append(
        run_one(
            "gemini",
            call_gemini,
            AssignmentPrompt,
            free_tier=True
        )
    )

    results.append(
        run_one(
            "groq",
            call_groq,
            AssignmentPrompt,
            free_tier=True
        )
    )

    print_table(results)

    # Save results in JSON format.
    with open("results.json", "w", encoding="utf-8") as file:

        json.dump(
            results,
            file,
            indent=4,
            ensure_ascii=False
        )

    print("\nResults saved successfully to results.json")


# --------------------------------------------------
# 9. Program entry point
# --------------------------------------------------

if __name__ == "__main__":
    main()

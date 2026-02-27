from openai import OpenAI
from fin_ai.core import config
from fin_ai.core.validation import is_finance_query

client = OpenAI(api_key=config.OPENAI_API_KEY)


DEFAULT_SYSTEM_PROMPT = (
    "You are a helpful financial assistant. Only provide information related to finance, investing, markets, "
    "stocks, portfolios, economic indicators, company fundamentals, or trading strategies. If the user asks "
    "about non-financial topics, politely refuse and suggest focusing on finance-related questions. "
    "When analyzing news, provide factual, neutral summaries and avoid speculation."
)


def chat_completion(prompt: str, model: str = "gpt-3.5-turbo") -> str:
    """Send prompt to OpenAI and return the assistant response.

    Enforces finance-only responses by adding a system prompt. If the user's prompt
    is non-financial (heuristic), return a polite refusal without calling OpenAI.
    """
    if not config.OPENAI_API_KEY:
        raise RuntimeError("OpenAI API key is not set")

    # Heuristic: if prompt not finance-related, refuse
    try:
        if not is_finance_query(prompt):
            return "I'm here to help with finance-related questions only. Please ask about markets, stocks, portfolios, or related financial topics."
    except Exception:
        pass

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": DEFAULT_SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            max_tokens=500,
            temperature=0.7,
        )
        return response.choices[0].message.get("content", "").strip()
    except Exception as e:
        # gracefully handle rate limit or other errors
        return f"[OpenAI error: {str(e)}]"


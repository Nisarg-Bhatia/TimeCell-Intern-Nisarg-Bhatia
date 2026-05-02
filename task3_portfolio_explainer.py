import os
import json
import argparse
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from google import genai
from google.genai import types

# import anthropic (Tried but got Credit limit even on 1st attempt in free tier)

from pydantic import BaseModel, Field
import dotenv

dotenv.load_dotenv()


class PortfolioExplanation(BaseModel):
    summary: str = Field(description="A 3-4 sentence plain-English summary of the portfolio's risk level.")
    doing_well: str = Field(description="One specific thing the investor is doing well.")
    consider_changing: str = Field(description="One specific thing the investor should consider changing, and why.")
    verdict: str = Field(description="A one-line verdict: 'Aggressive', 'Balanced', or 'Conservative'")

def explain_portfolio(portfolio: dict, tone: str = "friendly but honest"):
    """Generates a portfolio explanation using the Gemini API."""
    
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        Console().print("Key not found!")
        return None, None

    client = genai.Client(api_key=api_key)

    # api_key = os.environ.get("ANTHROPIC_API_KEY")
    # if not api_key:
    #     Console().print("Key not found!")
    #     return None, None

    # client = anthropic.Anthropic(api_key=api_key)


    prompt = f"""
    You are a {tone} financial advisor talking to a non-expert client. 
    Review the following portfolio and provide a risk assessment. 
    Speak directly to the client (e.g. "You have a...").

    Portfolio Details are as shown:
    {json.dumps(portfolio, indent=2)}
    """

    Console().print(f"Sending request to AI....")
    
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=PortfolioExplanation,
            ),
        )
        return response, json.loads(response.text)
    except Exception as e:
        Console().print(f"API Error: {e}")
        return None, None

    # try:
    #     response = client.messages.create(
    #         model="claude-sonnet-4-20250514",
    #         max_tokens=1024,
    #         messages=[{"role": "user", "content": prompt}],
    #     )
    #     raw_text = response.content[0].text
    #     return response, json.loads(raw_text)
    # except Exception as e:
    #     Console().print(f"API Error: {e}")
    #     return None, None

def main():
    parser = argparse.ArgumentParser(description="AI-Powered Portfolio Explainer")
    parser.add_argument(
        "--tone", 
        type=str, 
        choices=['beginner', 'experienced', 'expert'], 
        default='beginner',
        help="Adjust the tone of the explanation."
    )
    parser.add_argument(
    "--portfolio",
    type=str,
    default=None,
    help="Path to a JSON file containing the portfolio."
)
    args = parser.parse_args()

    # Map the CLI argument to a prompt description
    tone_map = {
        "beginner": "friendly, simple, and encouraging",
        "experienced": "professional, analytical, and honest",
        "expert": "highly technical, critical, and direct"
    }

    if args.portfolio:
        with open(args.portfolio, "r") as f:
            portfolio = json.load(f)
    else:
        Console().print("No portfolio file provided.")
        path = input("Enter path to your portfolio JSON file: ").strip()
        with open(path, "r") as f:
            portfolio = json.load(f)


    raw_response, parsed_response = explain_portfolio(portfolio, tone=tone_map[args.tone])

    if raw_response and parsed_response:
        # Print Raw Output
        Console().print("\nRaw API Response (in JSON):")
        Console().print(raw_response)
        
        Console().print("\n[bold cyan]=== Structured Portfolio Explanation ===[/bold cyan]")
        
        formatted_output = f"""
**Summary:** \n
{parsed_response['summary']}

**What You're Doing Well:** \n
{parsed_response['doing_well']}

**What To Consider Changing:** \n
{parsed_response['consider_changing']}

**Verdict:** \n
> {parsed_response['verdict']}
        """
        
        Console().print(Markdown(formatted_output))

if __name__ == "__main__":
    main()

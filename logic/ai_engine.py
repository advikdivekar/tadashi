import os
from dotenv import load_dotenv  # <--- NEW: Import the loader
from openai import OpenAI

# 1. Load the secrets IMMEDIATELY
load_dotenv()  # <--- NEW: Read .env before doing anything else

# 2. Initialize client (Now it will find the key)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def summarize_diff(diff_text):
    try:
        # Truncate if too long to save costs
        if len(diff_text) > 15000:
            diff_text = diff_text[:15000] + "\n...[Truncated]..."

        response = client.chat.completions.create(
            model="gpt-4o-mini", # or gpt-3.5-turbo
            messages=[
                {"role": "system", "content": "You are Tadashi, a helpful code reviewer. Summarize the changes in this git diff, explain why they matter, and politely point out any bugs or security risks. Use markdown."},
                {"role": "user", "content": f"Here is the diff:\n\n{diff_text}"}
            ]
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        return f"⚠️ **Neural Scan Failed:** {str(e)}"
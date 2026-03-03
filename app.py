import os
from fastapi import FastAPI, Request
import uvicorn
from dotenv import load_dotenv
from logic.github_client import handle_pr_event

load_dotenv()
app = FastAPI()

# We listen on BOTH paths to fix your 404 error
@app.post("/")
@app.post("/webhook")
async def handle_webhook(request: Request):
    try:
        payload = await request.json()
        
        # Check if it is a Pull Request
        if "pull_request" in payload:
            action = payload.get("action")
            if action == "opened":
                print(f"🤖 PR OPENED! Triggering Tadashi...")
                # Run the logic
                await handle_pr_event(payload)
                return {"status": "Analysis Started"}
            
        return {"status": "Ignored (Not an Opened PR)"}
        
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        return {"error": str(e)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3000)
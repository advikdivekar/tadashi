import os
from github import GithubIntegration
from logic.ai_engine import summarize_diff  # <--- Import the brain

async def handle_pr_event(payload):
    repo_name = payload["repository"]["full_name"]
    pr_number = payload["pull_request"]["number"]
    installation_id = payload["installation"]["id"]

    # 1. Authenticate
    app_id = os.getenv("APP_ID")
    private_key_path = os.getenv("PRIVATE_KEY_PATH")
    
    with open(private_key_path, 'r') as f:
        private_key = f.read()

    integration = GithubIntegration(app_id, private_key)
    gh = integration.get_github_for_installation(installation_id)
    repo = gh.get_repo(repo_name)
    pr = repo.get_pull(pr_number)

    # 2. Grab the Code Changes (The Diff)
    # We get the diff URL and fetch the raw text
    import requests
    diff_url = pr.diff_url
    response = requests.get(diff_url)
    diff_text = response.text

    # 3. Send to AI
    # Post a "Thinking..." comment first so the user knows we are working
    temp_comment = pr.create_issue_comment("🤖 **Tadashi is analyzing your code...** (Accessing Neural Network)")
    
    # Get the AI summary
    ai_summary = summarize_diff(diff_text)

    # 4. Update the comment with the result
    final_message = f"## 🤖 Tadashi Analysis\n\n{ai_summary}\n\n---\n*Be careful with those variables!*"
    temp_comment.edit(final_message)
    
    print(f"✅ SUCCESS: AI Summary posted on PR #{pr_number}")
import os
from dotenv import load_dotenv
from huggingface_hub import HfApi, login

# Load env
load_dotenv("trading_system/.env")

def verify_hf():
    token = os.getenv("HF_TOKEN") or os.getenv("HUGGINGFACEHUB_API_TOKEN")
    print(f"Checking HF Token...")
    
    if not token:
        print("❌ No HF_TOKEN found in .env")
        return

    try:
        # Try to login/access info
        login(token=token, add_to_git_credential=False)
        api = HfApi()
        user = api.whoami(token=token)
        print(f"\n✅ Authentication Successful!")
        print(f"User: {user['name']}")
        print(f"Type: {user['type']}")
        print(f"Permissions: {len(user.get('auth', {}).get('accessToken', {}).get('roles', []))} roles identified")

    except Exception as e:
        print(f"\n❌ Login Failed: {e}")

if __name__ == "__main__":
    verify_hf()

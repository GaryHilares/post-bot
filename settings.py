import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Use the environment variables
TOKEN = os.getenv("DISCORD_BOT_TOKEN")
ALLOWED_ROLE_ID_str = os.getenv("ALLOWED_ROLE_ID")
JOB_CHANNEL_ID_str = os.getenv("JOB_CHANNEL_ID")  # Channel ID for job postings
SERVICE_CHANNEL_ID_str = os.getenv(
    "SERVICE_CHANNEL_ID"
)  # Channel ID for service postings

# Convert environment variables to integers
ALLOWED_ROLE_ID = int(ALLOWED_ROLE_ID_str) if ALLOWED_ROLE_ID_str else None
JOB_CHANNEL_ID = int(JOB_CHANNEL_ID_str) if JOB_CHANNEL_ID_str else None
SERVICE_CHANNEL_ID = int(SERVICE_CHANNEL_ID_str) if SERVICE_CHANNEL_ID_str else None

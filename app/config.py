import os

from dotenv import load_dotenv
from pydantic import BaseModel


load_dotenv()

class Settings(BaseModel):
  """Load settings from environment variables."""

  OPENAI_API_KEY: str = ""
  GOOGLE_API_KEY: str = ""
  OPENAI_MODEL_NAME: str = "gpt-4.1"
  GOOGLE_MODEL_NAME: str = "gemini-2.5-flash"
  CONVEX_BASE_URL: str = ""


settings = Settings(
  OPENAI_API_KEY=os.getenv("OPENAI_API_KEY") or "",
  GOOGLE_API_KEY=os.getenv("GOOGLE_API_KEY") or "",
  OPENAI_MODEL_NAME=os.getenv("OPENAI_MODEL_NAME", "gpt-4.1"),
  GOOGLE_MODEL_NAME=os.getenv("GOOGLE_MODEL_NAME", "gemini-2.5-flash"),
  CONVEX_BASE_URL=os.getenv("CONVEX_BASE_URL") or "",
)

if not settings.OPENAI_API_KEY:
  raise ValueError("OPENAI_API_KEY is not set")

if not settings.GOOGLE_API_KEY:
  raise ValueError("GOOGLE_API_KEY is not set")

if not settings.CONVEX_BASE_URL:
  raise ValueError("CONVEX_BASE_URL is not set")

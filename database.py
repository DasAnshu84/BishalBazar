import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

SUPABASE_URL = os.getenv("PROJECT_URL_KEY")
SUPABASE_KEY = os.getenv("SERVICE_ROLE_KEY") # We use service role to bypass RLS for administrative CRUD if needed

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("Supabase database variables are missing in .env")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

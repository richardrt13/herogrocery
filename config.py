from dotenv import load_dotenv
import os

load_dotenv()

MONGODB_URI = st.secrets["mongo_uri"]
GOOGLE_API_KEY = st.secrets["api_key"]
DATABASE_NAME = "shopping_list_app"

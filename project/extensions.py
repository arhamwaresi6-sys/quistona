from flask_sqlalchemy import SQLAlchemy
from .settings import SUPABASE_KEY,SUPABASE_URL
from flask_login import LoginManager

from supabase import create_client
db = SQLAlchemy()
login_manager = LoginManager()
supabase = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)
import os
from flask import Flask
from dotenv import load_dotenv

# Load environment variables from .env if present
load_dotenv()

def init_db():
    import sqlite3
    db_dir = os.path.join(os.path.dirname(__file__), 'instance')
    os.makedirs(db_dir, exist_ok=True)
    db_path = os.path.join(db_dir, 'database.db')

    schema_path = os.path.join(os.path.dirname(__file__), 'database', 'schema.sql')
    if os.path.exists(schema_path):
        with open(schema_path, 'r', encoding='utf-8') as f:
            schema_sql = f.read()
        conn = sqlite3.connect(db_path)
        conn.executescript(schema_sql)
        conn.commit()
        conn.close()
        print("Database initialized successfully.")
    else:
        print("Cannot find schema.sql to initialize database.")

def create_app():
    from app.routes import main_bp, auth_bp, divination_bp, donation_bp

    flask_app = Flask(__name__, template_folder='app/templates', static_folder='app/static')
    flask_app.secret_key = os.environ.get('SECRET_KEY', 'default_dev_key_change_in_production')

    flask_app.register_blueprint(main_bp)
    flask_app.register_blueprint(auth_bp)
    flask_app.register_blueprint(divination_bp)
    flask_app.register_blueprint(donation_bp)

    return flask_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)

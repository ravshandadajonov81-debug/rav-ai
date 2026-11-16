f = open(".gitignore", "w", encoding="utf-8"); f.write(".env
__pycache__/
*.pyc
users_data.json
"); f.close(); print("OK!")
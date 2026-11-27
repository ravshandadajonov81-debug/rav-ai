toliq_royxat = """fastapi
uvicorn
groq
python-dotenv
httpx
duckduckgo-search
tzdata
geopy
timezonefinder
Babel
deep-translator
ddgs
apscheduler
pymongo
"""

with open('requirements.txt', 'w', encoding='utf-8') as f:
    f.write(toliq_royxat)

print("requirements.txt tozalab qayta yozildi!")
print(toliq_royxat)
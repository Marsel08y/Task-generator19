import os
import json
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app = FastAPI()
DB_FILE = "ratings.json"

if not os.path.exists(DB_FILE):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump([], f)

@app.get("/api/rating")
async def get_rating():
    with open(DB_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

@app.post("/api/rating")
async def save_rating(request: Request):
    data = await request.json()
    name, score = data.get("name"), data.get("s")
    if not name: return {"error": "no_name"}
    with open(DB_FILE, "r", encoding="utf-8") as f:
        records = json.load(f)
    user = next((r for r in records if r["name"].lower() == name.lower()), None)
    if user:
        if score > user["s"]: user["s"] = score
    else:
        records.append({"name": name, "s": score})
    records.sort(key=lambda x: x["s"], reverse=True)
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(records[:10], f, indent=2, ensure_ascii=False)
    return {"status": "ok"}

app.mount("/public", StaticFiles(directory="public"), name="public")

@app.get("/resilient-gumdrop-bbc7c5.netlify.app")
async def read_index():
    return FileResponse("public/index.html")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
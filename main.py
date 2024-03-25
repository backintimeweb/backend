import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "app.routes:app", host="0.0.0.0", port=8000, reload=True, debug=True, workers=3
    )

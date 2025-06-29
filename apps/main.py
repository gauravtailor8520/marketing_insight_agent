# Step 1: FastAPI app with /upload-csv and /run-agent
# File: app/main.py

from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse
import pandas as pd
import os
from agents.csv_loader import clean_csv
from agents.kg_ingest import ingest_to_neo4j
from agents.insight_generator import run_agent_pipeline

app = FastAPI()

# Temporary storage
CSV_STORAGE = "tmp/csvs"
os.makedirs(CSV_STORAGE, exist_ok=True)

@app.post("/upload-csv")
async def upload_csv(file: UploadFile = File(...)):
    try:
        file_path = os.path.join(CSV_STORAGE, file.filename)
        with open(file_path, "wb") as f:
            f.write(await file.read())
        df = clean_csv(file_path)
        ingest_to_neo4j(df)
        return {"message": "CSV uploaded and ingested to KG successfully"}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.post("/run-agent")
async def run_agent(question: str = Form(...), file_name: str = Form(...)):
    file_path = os.path.join(CSV_STORAGE, file_name)
    try:
        df = clean_csv(file_path)
        response = run_agent_pipeline(question, df)
        return {"answer": response["answer"], "evidence": response["evidence"]}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)







# # File: app/main.py
# """FastAPI entry point with routes to run the agent and upload CSVs."""

# from fastapi import FastAPI, UploadFile, File, Form
# from fastapi.middleware.cors import CORSMiddleware
# import pandas as pd
# from agents.insight_generator import run_agent_pipeline

# app = FastAPI(title="Marketing Insight Agent")

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


# @app.post("/run-agent")
# async def run_agent_route(
#     file: UploadFile = File(...),
#     question: str = Form(...),
# ):
#     df = pd.read_csv(file.file)
#     result = run_agent_pipeline(question=question, df=df)
#     return result


# @app.get("/")
# def root():
#     return {"message": "🚀 Marketing Insight Agent is up and running."}

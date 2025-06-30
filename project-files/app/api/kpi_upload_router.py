from fastapi import APIRouter, UploadFile, File, HTTPException
import os
import traceback

# Create upload directory if it doesn't exist
UPLOAD_DIR = "uploaded_kpis"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Initialize router
kpi_upload_router = APIRouter()

# Route: POST /upload-doc
@kpi_upload_router.post("/upload-doc", tags=["KPI Upload"])
async def upload_doc(file: UploadFile = File(...)):
    try:
        file_location = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_location, "wb") as f:
            f.write(await file.read())
        return {"message": f"File '{file.filename}' uploaded successfully."}
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
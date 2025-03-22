from fastapi import FastAPI, File, UploadFile, HTTPException, BackgroundTasks # type: ignore
from pydantic import BaseModel # type: ignore
import os
from scripts.speech2text import transcribe_audio
from scripts.extract_data import ask_llm
from scripts.save_data import save_to_google_sheets
from scripts.send_email import send_email_notification
import shutil

# Initialize FastAPI app
app = FastAPI()

# Temporary folder for storing uploaded files
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


# 🔹 API 1: Transcribe Audio (Whisper)
@app.post("/transcribe/")
async def transcribe_audio_file(file: UploadFile = File(...)):
    try:
        print('open transcribe')
        file_path = os.path.join(UPLOAD_DIR, file.filename)

        # Save the uploaded file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Transcribe the audio
        transcript = transcribe_audio(file_path)

        # Cleanup: Remove the temporary file
        os.remove(file_path)

        return {"transcript": transcript}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error transcribing audio: {str(e)}")


# 🔹 API 2: Extract Meeting Details (LLM)
class TranscriptData(BaseModel):
    transcript: str

@app.post("/extract/")
async def extract_meeting_details(data: TranscriptData):
    try:
        extracted_data = ask_llm(data.transcript)
        if data.transcript:
            extracted_data["transcript"] = data.transcript
        return extracted_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error extracting data: {str(e)}")


# 🔹 API 3: Save Data to Google Sheets

class MeetingData(BaseModel):
    name: str
    start_time: str
    end_time: str
    total_hours: str
    meeting_date: str
    note: str

    class Config:
        extra = "allow" 

@app.post("/save/")
async def save_meeting_data(data: MeetingData):
    try:
        save_to_google_sheets(data.dict())
        return {"message": "Data saved successfully!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving to Google Sheets: {str(e)}")


# 🔹 API 4: Send Email Notification (Background Task)
@app.post("/notify/")
async def send_email(data: MeetingData, background_tasks: BackgroundTasks):
    try:
        # Send email in the background (non-blocking)
        background_tasks.add_task(send_email_notification, data.dict())

        return {"message": "Email notification sent!"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error sending email: {str(e)}")


from datetime import datetime

@app.post("/upload/")
async def upload_and_process_audio(file: UploadFile = File(...), background_tasks: BackgroundTasks = None):
    try:
        file_path = os.path.join(UPLOAD_DIR, file.filename)

        # 1. Save the file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # 2. Transcribe audio
        transcript = transcribe_audio(file_path)

        # 3. Extract data
        extracted_data = ask_llm(transcript)
        extracted_data["transcript"] = transcript
     

        # 5. Save to Google Sheets
        save_to_google_sheets(extracted_data)

        # 6. Send email (non-blocking)
        if background_tasks:
            background_tasks.add_task(send_email_notification, extracted_data)

        # 7. Clean up
        os.remove(file_path)

        return {
            "message": "Audio processed successfully",
            "transcript": transcript,
            "extracted_data": extracted_data
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload processing failed: {str(e)}")



# Run the API
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)

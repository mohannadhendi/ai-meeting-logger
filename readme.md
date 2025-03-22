# 📁 AI Meeting Logger - Automate Work Hours with Voice AI

Turn every **meeting conversation into structured data—automatically!**
With **FastAPI, Whisper, and LangChain**, this project helps consultants and teams log **meeting summaries, participants, and key insights** directly from voice recordings. All **saved to Google Sheets** and fully automated via **n8n workflows**.

---

## 🌟 Key Features

- ✅ **Upload voice notes** via API or n8n webhook
- ✅ **Transcribe audio** to text using Whisper
- ✅ **Extract meeting details** using LLM-powered insights
- ✅ **Save structured data** in Google Sheets
- ✅ **Send email notifications** after each entry
- ✅ **Automate workflow** seamlessly with n8n

---

## 🚀 How It Works (End-to-End Workflow)

1. **Voice Upload** → Upload `.mp3` file via API or n8n webhook
2. **Transcription** → Whisper converts audio to text
3. **Info Extraction** → LangChain + Ollama extracts meeting details
4. **Google Sheets Logging** → Meeting data is appended
5. **Email Notification** → Summary is emailed 
6. **n8n Orchestration** → End-to-end process automation

📌 **Fully automated workflow** - Just upload a file & let AI handle the rest!

---

## 🛠 Technologies Used

- **FastAPI** - Backend API service
- **OpenAI Whisper** - Audio-to-text engine
- **LangChain + Ollama** - LLM-driven extraction
- **Google Sheets API** - Structured database
- **n8n** - Low-code automation

---

## 🔧 FastAPI Endpoints

### 1️⃣ `/upload/` – Upload and Process Audio
- Accepts: `.mp3` file
- Runs the full pipeline:
  - Transcribes audio
  - Extracts info
  - Adds transcript to result
  - Saves to Google Sheets
  - Sends email 

### 2️⃣ `/transcribe/`
- Input: `.mp3` audio file
- Output: transcript (text)

### 3️⃣ `/extract/`
- Input: JSON with `transcript`
- Output: Extracted fields like `name`, `start_time`, `note`, etc.

### 4️⃣ `/save/`
- Input: JSON object with meeting fields
- Output: Saves a row to Google Sheets

### 5️⃣ `/notify/`
- Input: Same JSON as `/save/`
- Action: Sends formatted email with extracted info

---

## 🟢 Local Setup Instructions

### ✅ 1. Clone and Setup
```bash
git clone https://github.com/yourusername/ai-meeting-logger.git
cd ai-meeting-logger
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### ✅ 2. Run the App
```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

### ✅ 3. Test Endpoints
Use **Postman**, **cURL**, or browser to access:
- [http://localhost:8000/docs](http://localhost:8000/docs) → interactive Swagger UI

---

## 🔄 Workflow Automation (n8n)

You can trigger the pipeline automatically using n8n.

### 🔹 **Uploading JSON Files to n8n**
1. Open **n8n** and create a new workflow.
2. Add a **Webhook** node to accept incoming JSON files.
3. Upload your meeting data JSON file.
4. Pass the data through the following nodes:
   - **HTTP Request (Transcribe)** → Sends audio to `/transcribe/`
   - **HTTP Request (Extract)** → Sends transcript to `/extract/`
   - **HTTP Request (Save)** → Saves structured data
   - **HTTP Request (Notify)** → Sends summary email

### Sample Workflow:

1. **Webhook Node** - Accepts voice note from client
2. **HTTP Request (Transcribe)** - Sends audio to `/transcribe/`
3. **HTTP Request (Extract)** - Sends transcript to `/extract/`
4. **HTTP Request (Save) & Notify** - Parallel saving and emailing

---

## 📄 Environment Configuration

Create a `.env` file in root directory:

```env
LANGCHAIN_API_KEY=langchain_api_key
LANGCHAIN_TRACING_V2=true
LANGCHAIN_ENDPOINT=https://api.smith.langchain.com
SERVICE_ACCOUNT_FILE=path_to_your_service_account.json
SPREADSHEET_ID=your_google_sheet_id
WORKSHEET_NAME=Sheet1
EMAIL_SENDER=example@gmail.com
EMAIL_PASSWORD=your_app_password
EMAIL_RECEIVER=target_email@gmail.com
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
```

---

## 📂 Project Structure

```
📁 asal_project
├── app.py               # FastAPI main file
├── requirements.txt
├── .env
├── uploads/             # Uploaded audio temp storage
├── scripts/
│   ├── speech2text.py
│   ├── extract_data.py
│   ├── save_data.py
│   └── send_email.py
```

---

## 📖 References

- 📌 **[n8n Documentation](https://docs.n8n.io/)**
- 📌 **[LangChain + Ollama Documentation](https://python.langchain.com/docs/modules/model_io/models/llms/integrations/ollama/)**
- 📌 **[FastAPI Documentation](https://fastapi.tiangolo.com/)**
- 📌 **[Whisper Speech-to-Text](https://github.com/openai/whisper)**
- 📌 **[Google Sheets API](https://developers.google.com/sheets/api/guides/concepts)**
- 📌 **GPT-4 for Research and Document Organization**


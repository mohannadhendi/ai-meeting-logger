from langchain_ollama import ChatOllama # type: ignore
from langchain_core.prompts import (SystemMessagePromptTemplate,  # type: ignore
                                    HumanMessagePromptTemplate,
                                    ChatPromptTemplate)
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser # type: ignore
import re

#  Define LLM Configuration
base_url = "http://localhost:11434"
model = 'llama3.2:3b'

llm = ChatOllama(base_url=base_url, model=model)

# System Message for Context
system = SystemMessagePromptTemplate.from_template(
    "You are an AI assistant that extracts structured data from meeting transcripts in JSON format."
)

#  Refined Prompt for JSON Extraction
json_prompt = """
**Task:** Extract key information from the following text.

**Transcript Text:**
{context}

**Instructions:**
1. For the customer name, look for an introduction phrase such as "Hi, this is [Name]" or "Hello, this is [Name]". Extract only the name (e.g., "Sarah"). If no name is mentioned, return an empty string.
2. For start and end times, extract them ONLY if explicitly mentioned in the text (e.g., '3:15 PM' or '4:45 PM'). If they are not clearly stated, return empty strings.
3. If total hours is explicitly stated (e.g., "lasting 1.5 hours"), include it. Otherwise, leave it empty.
4. For the meeting date, extract it if present; otherwise, default to today's date.
5. Extract any additional meeting notes provided.

Return ONLY a valid JSON object without any additional text, using the following format:

```json
{{
    "name": "<Extracted Customer Name or empty string>",
    "start_time": "<Extracted Start Time (e.g., '3:15 PM') or empty string>",
    "end_time": "<Extracted End Time (e.g., '4:45 PM') or empty string>",
    "total_hours": "<Total meeting hours. If not provided, calculate from start and end times>",
    "meeting_date": "<Extracted Meeting Date or today's date if missing>",
    "note": "<Extracted Meeting Notes>"
}}
"""
prompt = HumanMessagePromptTemplate.from_template(json_prompt)




def fix_time_format(transcript):
    """
    Fixes time formats where Whisper removes colons.
    - Converts '315 PM' -> '3:15 PM'
    - Converts '3 PM' -> '3:00 PM'
    - Handles time intervals like '315 PM to 445 PM' -> '3:15 PM to 4:45 PM'
    """
    # Step 1: Fix missing colons in full times (e.g., "315 PM" -> "3:15 PM")
    pattern_full = r'\b(\d{1,2})(\d{2})\s?(AM|PM|am|pm)\b'
    
    def add_colon(match):
        hours, minutes, period = match.groups()
        return f"{int(hours)}:{minutes} {period.upper()}"

    transcript = re.sub(pattern_full, add_colon, transcript)
    
    # Step 2: Fix single-hour times missing minutes (e.g., "3 PM" -> "3:00 PM")
    # Use a negative lookahead (?!:) to ensure we don't modify times that already have a colon.
    pattern_single = r'\b(\d{1,2})(?!:)\s*(AM|PM|am|pm)\b'
    transcript = re.sub(pattern_single, r'\1:00 \2', transcript)
    
    return transcript


#  Function to Call LLM
def ask_llm(context):

    fixed_context = fix_time_format(context)
    messages = [system, prompt]
    template = ChatPromptTemplate(messages)

    qna_chain = template | llm | JsonOutputParser()  #  Ensure Output is Always JSON
    return qna_chain.invoke({'context': fixed_context})



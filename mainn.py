from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from google_calendar import authenticate_google_calendar, check_availability, create_event
from helper import parse_prompt

app = FastAPI()

# Define a Pydantic model for the request body
class MeetingRequest(BaseModel):
    prompt: str

@app.post("/book-meeting/")
async def book_meeting(request: MeetingRequest):
    try:
        # Step 1: Parse the prompt
        recipient_email, start_time, end_time = parse_prompt(request.prompt)

        # Step 2: Authenticate with Google Calendar
        service = authenticate_google_calendar()

        # Step 3: Check availability
        if not check_availability(service, recipient_email, start_time, end_time):
            raise HTTPException(status_code=400, detail="Recipient is not available at the specified time.")

        # Step 4: Create the event
        event_link = create_event(
            service,
            organizer_email="s.mehrab@nextgeni.com",  # Replace with your email
            attendee_email=recipient_email,
            start_time=start_time,
            end_time=end_time
        )

        return {"message": "Meeting booked successfully!", "event_link": event_link}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
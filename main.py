from fastapi import FastAPI, Body, HTTPException, Request
import asyncio
from models import Event, Artist, EventCreate, EventBase 
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

class RequestBody(BaseModel):
    reqBody: str
EVENTS = [
    {"id":1, "name":"Xmas", "venue": "Bangalore","artist": {"name":"DJ Ivan", "age": 30, "genre": "Bollywood"}},
    {"id":2, "name":"NYE", "venue": "Delhi", "artist": {"name":"DJ Aryan", "age": 25, "genre": "EDM"}},
    {"id":3, "name":"Halloween", "venue": "Bangalore", "artist": {"name":"DJ Deleef", "age": 35, "genre": "Hollywood"}},
    {"id":4, "name":"Holi", "venue": "Mumbai", "artist": {"name":"DJ Prithvi", "age": 40, "genre": "Bollywood"}},
    {"id":5, "name":"Freshers", "venue": "Bangalore", "artist": {"name":"DJ Raghu", "age": 22, "genre": "EDM"}},
    {"id":6, "name":"AFTERPARTY", "venue": "Mumbai", "artist": {"name":"DJ Vasisth", "age": 28, "genre": "Hollywood"}},
    {"id":7, "name":"Garba", "venue": "Delhi", "artist": {"name":"DJ Trave", "age": 32, "genre": "Bollywood"}},
    {"id":8, "name":"Kareoke", "venue": "Bangalore", "artist": {"name":"DJ Ziona", "age": 26, "genre": "EDM"}},
]

@app.get("/")
async def getMethodRoot() -> str:
    return "/ route"

# query parameter : name
@app.get("/events")
async def routeOne(name: str | None = None) -> list[Event]:
    if name:
        return [Event(**e) for e in EVENTS if e["name"].lower() == name.lower()]
    return [Event(**e) for e in EVENTS]

@app.get("/events/{event_id}")
async def getEventDetails(event_id : int) -> Event:
	for event in EVENTS:
		if event["id"] == event_id:
			return Event(**event)
	raise HTTPException(status_code=404, detail="event not found")

@app.get("/events/venue/{venue_name}")
async def getAllVenues(venue_name : str) -> list[Event]:
	allVenuesList = []
	for event in EVENTS:
		if event["venue"].lower() == venue_name.lower():
			allVenuesList.append(Event(**event))
	if allVenuesList == []:
		raise HTTPException(status_code=404, detail="No venue Found")
	else:
		return allVenuesList
		
# Request Body with POST method

@app.post("/events")
async def create_event(
    event_request_body: Optional[EventCreate] = Body(None, description="Event details in the request body")
) -> Event:
    # Check if the body is missing
    if event_request_body is None:
        raise HTTPException(
            status_code=400,
            detail="Request body is missing, valid event data.",
        )
    
    new_id = EVENTS[-1]["id"] + 1
    new_event = {"id": new_id, **event_request_body.dict()}
    EVENTS.append(new_event)
    return Event(**new_event)


@app.post("/test")
async def testMethod(reqBody: str = Body(..., embed=False)) -> str:
    return "Jinja Template" + reqBody

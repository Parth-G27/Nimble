from pydantic import BaseModel

class Artist(BaseModel):
    name: str
    age: int
    genre: str

class EventBase(BaseModel):
    name: str
    venue: str
    artist: Artist

class EventCreate(EventBase):
    pass 

class Event(EventBase):
    id : int 

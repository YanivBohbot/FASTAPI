from typing import List
from fastapi import APIRouter, HTTPException, status
from models.events import Event, EventUpdate
from database.connections import Database
from beanie import PydanticObjectId


event_router = APIRouter(tags=["Event"])

events_database = Database(Event)


@event_router.get("/", response_model=List[Event])
async def retrieve_all_events() -> List[Event]:
    events = await events_database.get_all()
    return events


@event_router.get("/{id}", response_model=Event)
async def retrieve_event(id: PydanticObjectId) -> Event:
    event = await events_database.get(id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event with supplied ID does not exist",
        )
    return event


@event_router.post("/new")
async def create_event(body: Event) -> dict:
    await events_database.save(body)
    return {"message": "Event created succesufully"}


@event_router.delete("/{id}")
async def delete_events(id: PydanticObjectId) -> dict:
    event = await events_database.delete(id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event with supplied ID doest not exist",
        )
    return {"message": "Event deleted success !"}


@event_router.put("/{id}", response_model=Event)
async def update_event(id: PydanticObjectId, body: EventUpdate) -> Event:
    update_event = await events_database.update(id, body)

    if not update_event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Event with id does not exist"
        )
    return update_event

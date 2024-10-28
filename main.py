from fastapi import FastAPI
from domain.message import MessageRequest
from rag import agent

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

from tasks import ingest_data_task

scheduler = BackgroundScheduler()
trigger = CronTrigger(hour="0", minute="0")

app = FastAPI()

scheduler.add_job(ingest_data_task, trigger)
scheduler.start()


@app.get("/healthcheck")
async def healthcheck():
    return {"status": "ok"}


@app.post("/chat")
async def chat(message_request: MessageRequest):
    response = agent.message(message_request.message)
    return {
        "assistant": response,
    }


@app.post("/force-indexation")
def force_indexation():
    ingest_data_task()
    return {
        "message": "Force indexation started!",
    }

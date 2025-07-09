import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.api.v1.endpoints.location import router as location_router
from src.api.v1.endpoints.story import router as story_router
from src.config import Settings
from src.utils import cacheClearer
from fastapi.middleware.cors import CORSMiddleware


def get_settings():
    return Settings()


settings = get_settings()

# Store background tasks
background_tasks = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Create background task for cache clearing
    task = asyncio.create_task(cacheClearer.periodic_cache_clear())
    background_tasks["location_cache_clearer"] = task
    yield
    # Shutdown: Cancel background tasks
    for task_name, task in background_tasks.items():
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            print(f"Background task {task_name} cancelled")


app = FastAPI(title=settings.app_name if settings.app_name != None else "Echoes app, check app name config",
              debug=settings.debug,
              version="1.0.0", lifespan=lifespan)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://history-echoes.se", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    location_router,
    prefix="/api/v1",
    tags=["location"]
)

app.include_router(
    story_router,
    prefix="/api/v1",
    tags=["story"]
)


@app.get("/")
def read_root():
    return {
        "app": settings.app_name,
        "environment": settings.environment,
        "debug": settings.debug
    }

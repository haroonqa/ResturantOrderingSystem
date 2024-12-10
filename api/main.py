import uvicorn
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .routers import index as indexRoute
from .models import model_loader
from .dependencies.config import conf
from .routers.orders import router as orders_router
from .routers.ingredient_tracking import router as inventory_router
from .routers.menu_search import router as menu_search_router
from .routers.menu_analytics import router as menu_analytics_router



app = FastAPI()

app.include_router(orders_router)
app.include_router(inventory_router)
app.include_router(menu_search_router)
app.include_router(menu_analytics_router)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model_loader.index()
indexRoute.load_routes(app)

@app.get("/")
async def root():
    return {"message": "Welcome to the Restaurant Ordering System!"}

if __name__ == "__main__":
    uvicorn.run(app, host=conf.app_host, port=conf.app_port)
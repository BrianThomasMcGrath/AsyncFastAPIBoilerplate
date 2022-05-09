from fastapi.routing import APIRouter
from app.api.v1.games import router as game_router
from app.api.v1.teams import router as team_router

router = APIRouter()
router.include_router(game_router)
router.include_router(team_router)

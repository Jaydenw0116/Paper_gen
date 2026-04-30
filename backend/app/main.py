from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from .api.routes import router
import os

app = FastAPI(
    title="坚哥小测组卷系统v1.0 API",
    description="基于Word底层XML的智能组卷系统后端API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api")

# 提供前端静态文件服务（使用构建后的 dist 目录）
frontend_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "frontend", "dist")
app.mount("/", StaticFiles(directory=frontend_dir, html=True), name="frontend")
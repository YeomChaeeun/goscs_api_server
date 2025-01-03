from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 실제 배포시에는 특정 도메인만 허용하도록 수정
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello World_test"}

# 추가 라우트
@app.get("/api/items")
async def get_items():
    return {"items": ["item1", "item2"]}

# Vercel은 ASGI 애플리케이션을 위해 app 객체를 찾습니다
from fastapi import FastAPI
import uvicorn
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware

import api.service as service

app = FastAPI()

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 실제 배포시에는 특정 도메인만 허용하도록 수정
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/",include_in_schema=False)
async def docs_redirect():
    return RedirectResponse(url = "/docs", status_code = 302)


@app.get("/api/news")
async def get_news(item_name:str, item_count:int = 5):
    news_result = service.get_news(item_name, item_count)
    
    return news_result


if __name__ == "__main__":
    uvicorn.run(app)
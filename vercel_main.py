from fastapi import FastAPI, HTTPException
import uvicorn
from fastapi.responses import RedirectResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import mimetypes
from typing import Optional

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

def get_mime_type(filename: str) -> Optional[str]:
    """파일의 MIME 타입 반환"""
    return mimetypes.guess_type(filename)[0]

@app.get("/api/adjusted_close_graph")
async def get_adjested_close_graph(item_code_list:str, duration_str:str = None):
    
    image_path = service.get_adjusted_close_graph(item_code_list.split(","), duration_str)
    
    # 기본적인 유효성 검사
    if not os.path.exists(image_path):
        raise HTTPException(status_code=404, detail="Image not found")
    
    
    try:
        # 파일의 MIME 타입 확인
        mime_type = get_mime_type(image_path)
        if not mime_type:
            raise HTTPException(status_code=400, detail="Invalid file type")
        
        # 파일이 읽기 가능한지 확인
        if not os.access(image_path, os.R_OK):
            raise HTTPException(status_code=500, detail="File not accessible")
        
        # FileResponse 생성
        response = FileResponse(
            image_path,
            media_type=mime_type,
        )
        
        # 파일 삭제 시도
        #try:
        #    os.remove(image_path)
        #except OSError as e:
        #    print(f"Warning: Failed to delete file {image_path}: {e}")
            # 파일 삭제 실패는 사용자에게 영향을 주지 않도록 함
        
        return response
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing image: {str(e)}"
        )


if __name__ == "__main__":
    uvicorn.run(app)
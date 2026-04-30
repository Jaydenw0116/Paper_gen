from fastapi import APIRouter, File, UploadFile, HTTPException, BackgroundTasks
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List
import uuid
from io import BytesIO

from ..core.xml_parser import QuestionParser
from ..core.xml_composer import DocumentComposer
from ..core.cache import cache_manager
from ..core.config import settings

router = APIRouter()

class QuestionItem(BaseModel):
    id: str
    original_no: str
    preview_text: str
    images: List[str]

class ComposeRequest(BaseModel):
    session_id: str
    question_ids: List[str]
    title: str = "试卷"
    subject: str = ""
    total_score: int = 100

@router.post("/upload", response_model=dict)
async def upload_documents(
    question_file: UploadFile = File(...),
    answer_file: UploadFile = File(...)
):
    if question_file.content_type not in ["application/vnd.openxmlformats-officedocument.wordprocessingml.document", "application/octet-stream"]:
        raise HTTPException(status_code=400, detail="题目文档必须是.docx格式")
    
    if answer_file.content_type not in ["application/vnd.openxmlformats-officedocument.wordprocessingml.document", "application/octet-stream"]:
        raise HTTPException(status_code=400, detail="答案文档必须是.docx格式")
    
    question_content = await question_file.read()
    answer_content = await answer_file.read()
    
    if len(question_content) > settings.max_file_size:
        raise HTTPException(status_code=400, detail="题目文档大小超过限制")
    
    if len(answer_content) > settings.max_file_size:
        raise HTTPException(status_code=400, detail="答案文档大小超过限制")
    
    questions = QuestionParser.parse_document(question_content)
    
    question_items = []
    session_id = cache_manager.generate_session_id()
    
    for idx, q in enumerate(questions):
        q_id = str(uuid.uuid4())
        q_bytes = QuestionParser.extract_question_block(question_content, q['start'], q['end'])
        preview_text = QuestionParser.extract_preview_text(q_bytes)
        images = QuestionParser.extract_images(q_bytes)
        
        cache_manager.set_docx_bytes(f"session:{session_id}:question:{q_id}", q_bytes)
        
        answer_bytes = QuestionParser.extract_question_block(answer_content, q['start'], q['end'])
        cache_manager.set_docx_bytes(f"session:{session_id}:answer:{q_id}", answer_bytes)
        
        question_items.append({
            "id": q_id,
            "original_no": q['number'],
            "preview_text": preview_text,
            "images": images
        })
    
    cache_manager.set_questions(session_id, question_items)
    cache_manager.expire_session(session_id, 3600)
    
    return {"session_id": session_id, "questions": question_items}

@router.get("/questions/{session_id}", response_model=List[QuestionItem])
async def get_questions(session_id: str):
    questions = cache_manager.get_questions(session_id)
    if not questions:
        raise HTTPException(status_code=404, detail="会话不存在或已过期")
    return questions

@router.post("/compose")
async def compose_documents(request: ComposeRequest):
    questions = cache_manager.get_questions(request.session_id)
    if not questions:
        raise HTTPException(status_code=404, detail="会话不存在或已过期")
    
    if len(request.question_ids) > settings.max_questions:
        raise HTTPException(status_code=400, detail="单次组卷题目数量超过限制")
    
    question_bytes_list = []
    answer_bytes_list = []
    
    for idx, q_id in enumerate(request.question_ids):
        q_bytes = cache_manager.get_docx_bytes(f"session:{request.session_id}:question:{q_id}")
        a_bytes = cache_manager.get_docx_bytes(f"session:{request.session_id}:answer:{q_id}")
        
        if not q_bytes or not a_bytes:
            raise HTTPException(status_code=404, detail=f"题目ID {q_id} 不存在")
        
        q_bytes = DocumentComposer.renumber_question(q_bytes, idx + 1)
        a_bytes = DocumentComposer.renumber_question(a_bytes, idx + 1)
        
        question_bytes_list.append(q_bytes)
        answer_bytes_list.append(a_bytes)
    
    template_bytes = DocumentComposer.create_empty_template()
    paper_doc = DocumentComposer.compose_documents(template_bytes, question_bytes_list)
    answer_doc = DocumentComposer.compose_documents(template_bytes, answer_bytes_list)
    
    cache_manager.set_docx_bytes(f"session:{request.session_id}:paper", paper_doc)
    cache_manager.set_docx_bytes(f"session:{request.session_id}:answer", answer_doc)
    
    return {"message": "组卷成功"}

@router.get("/download/{session_id}/{doc_type}")
async def download_document(session_id: str, doc_type: str):
    if doc_type not in ["paper", "answer"]:
        raise HTTPException(status_code=400, detail="无效的文档类型")
    
    doc_bytes = cache_manager.get_docx_bytes(f"session:{session_id}:{doc_type}")
    if not doc_bytes:
        raise HTTPException(status_code=404, detail="文档不存在或已过期")
    
    filename = "试卷.docx" if doc_type == "paper" else "答案.docx"
    
    return StreamingResponse(
        BytesIO(doc_bytes),
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )

@router.delete("/session/{session_id}")
async def delete_session(session_id: str):
    cache_manager.delete_session(session_id)
    return {"message": "会话已删除"}
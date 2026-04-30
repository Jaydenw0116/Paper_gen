import re
import uuid
import base64
from io import BytesIO
from docx import Document
from docx.oxml.ns import qn
from docx.oxml import OxmlElement, parse_xml
from docx.shared import Inches
from typing import List, Dict, Any, Tuple

class QuestionParser:
    QUESTION_NUMBER_REGEX = re.compile(r'^\s*\d+[\.．、](?!\d)')
    
    @staticmethod
    def parse_document(doc_bytes: bytes) -> List[Dict[str, Any]]:
        doc = Document(BytesIO(doc_bytes))
        questions = []
        
        current_question = []
        current_number = None
        question_start = 0
        
        for i, element in enumerate(doc.element.body):
            if element.tag.endswith('p'):
                text = QuestionParser._get_element_text(element)
                match = QuestionParser.QUESTION_NUMBER_REGEX.match(text)
                if match and current_question:
                    questions.append({
                        'start': question_start,
                        'end': i,
                        'number': current_number,
                        'text': '\n'.join(current_question)
                    })
                    current_question = [text]
                    current_number = match.group().strip()
                    question_start = i
                elif match:
                    current_question = [text]
                    current_number = match.group().strip()
                    question_start = i
                elif current_question:
                    current_question.append(text)
            elif element.tag.endswith('tbl') and current_question:
                current_question.append('[TABLE]')
        
        if current_question:
            questions.append({
                'start': question_start,
                'end': len(doc.element.body),
                'number': current_number,
                'text': '\n'.join(current_question)
            })
        
        return questions

    @staticmethod
    def _get_element_text(element) -> str:
        text_parts = []
        for child in element.iter():
            if child.tag.endswith('t'):
                text_parts.append(child.text or '')
            elif child.tag.endswith('tab'):
                text_parts.append(' ')
        return ''.join(text_parts)

    @staticmethod
    def extract_question_block(doc_bytes: bytes, start_idx: int, end_idx: int) -> bytes:
        doc = Document(BytesIO(doc_bytes))
        
        for i in range(len(doc.element.body) - 1, end_idx - 1, -1):
            if not doc.element.body[i].tag.endswith('sectPr'):
                doc.element.body.remove(doc.element.body[i])
        
        for i in range(start_idx - 1, -1, -1):
            if not doc.element.body[i].tag.endswith('sectPr'):
                doc.element.body.remove(doc.element.body[i])
        
        last_child = doc.element.body[-1]
        if last_child is not None and not last_child.tag.endswith('sectPr'):
            new_p = OxmlElement('w:p')
            doc.element.body.insert(len(doc.element.body) - 1, new_p)
        
        output = BytesIO()
        doc.save(output)
        return output.getvalue()

    @staticmethod
    def extract_preview_text(doc_bytes: bytes) -> str:
        doc = Document(BytesIO(doc_bytes))
        text = []
        
        for element in doc.element.body:
            if element.tag.endswith('p'):
                text.append(QuestionParser._get_element_text(element))
            elif element.tag.endswith('tbl'):
                text.append('[TABLE]')
        
        full_text = '\n'.join(text)
        full_text = re.sub(r'\b\d{9,}\b', '', full_text)
        return full_text.strip()[:500]

    @staticmethod
    def extract_images(doc_bytes: bytes) -> List[str]:
        images = []
        doc = Document(BytesIO(doc_bytes))
        
        for rel in doc.part.rels.values():
            if 'image' in rel.target_ref:
                image_data = rel.target_part.blob
                if image_data:
                    base64_img = base64.b64encode(image_data).decode('utf-8')
                    images.append(base64_img)
        
        return images
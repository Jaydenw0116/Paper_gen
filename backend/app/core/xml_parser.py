import re
from io import BytesIO
from docx import Document
from docx.oxml import OxmlElement
from typing import List, Dict, Any


class QuestionParser:
    """
    简化的问题解析器，模仿app.py的思路
    """

    @staticmethod
    def parse_document(doc_bytes: bytes) -> List[Dict[str, Any]]:
        """
        解析文档，提取问题块
        返回: [{'start': int, 'end': int, 'number': str, 'text': str}]
        """
        doc = Document(BytesIO(doc_bytes))
        body = doc.element.body
        
        # 收集所有题号位置
        q_indices = []
        for i, child in enumerate(body):
            if child.tag.endswith("p") or child.tag.endswith("tbl"):
                text = QuestionParser._get_clean_text(child)
                # 匹配题号（排除小数如0.5中的0.）
                if re.match(r"^\s*\d+[\.．、](?!\d)", text):
                    q_indices.append(i)
        
        if not q_indices:
            return []
        
        # 添加文档末尾作为最后一个结束位置
        q_indices.append(len(body))
        
        # 按位置范围切分问题
        questions = []
        for k in range(len(q_indices) - 1):
            start_idx = q_indices[k]
            end_idx = q_indices[k + 1]
            
            # 获取题号
            start_element = body[start_idx]
            start_text = QuestionParser._get_clean_text(start_element)
            no_match = re.match(r"^\s*(\d+)[\.．、]", start_text)
            original_no = no_match.group(1) + '.' if no_match else str(k + 1) + '.'
            
            questions.append({
                'start': start_idx,
                'end': end_idx,
                'number': original_no,
                'text': start_text[:100] + '...'
            })
        
        return questions

    @staticmethod
    def _get_clean_text(element) -> str:
        """获取元素的纯文本内容，跳过图片等drawing元素"""
        text_parts = []
        
        def traverse(node, inside_drawing=False):
            tag = node.tag.lower() if hasattr(node, 'tag') else ''
            is_drawing = (
                inside_drawing
                or 'drawing' in tag
                or 'shape' in tag
                or 'alternatecontent' in tag
            )
            
            if tag.endswith('t') and node.text and not is_drawing:
                text_parts.append(node.text)
            elif tag.endswith('tab') and not is_drawing:
                text_parts.append(' ')
            
            if hasattr(node, '__iter__'):
                for child in node:
                    traverse(child, is_drawing)
        
        traverse(element)
        return ''.join(text_parts).strip()

    @staticmethod
    def extract_question_block(doc_bytes: bytes, start_idx: int, end_idx: int, question_number: str = None) -> bytes:
        """
        提取指定范围的问题块，保留格式和图片
        """
        new_doc = Document(BytesIO(doc_bytes))
        new_body = new_doc.element.body
        
        # 删除不在范围内的元素
        for i in range(len(new_body) - 1, -1, -1):
            child = new_body[i]
            # 保留sectPr（节属性）
            if child.tag.endswith("sectPr"):
                continue
            # 删除范围外的元素
            if i < start_idx or i >= end_idx:
                child.getparent().remove(child)
        
        # 在末尾添加一个空段落（避免文档损坏）
        para = new_doc.add_paragraph()
        p_elem = para._p
        sect_prs = new_body.xpath("./w:sectPr")
        if sect_prs:
            sect_prs[-1].addprevious(p_elem)

        output = BytesIO()
        new_doc.save(output)
        return output.getvalue()

    @staticmethod
    def extract_preview_text(doc_bytes: bytes) -> str:
        """提取文档的预览文本"""
        doc = Document(BytesIO(doc_bytes))
        text_parts = []
        for para in doc.paragraphs[:3]:
            text_parts.append(para.text)
        return ' '.join(text_parts).strip()[:200]

    @staticmethod
    def extract_images(doc_bytes: bytes) -> List[str]:
        """提取文档中的图片信息"""
        doc = Document(BytesIO(doc_bytes))
        images = []
        for rel in doc.part.rels.values():
            if "image" in rel.target_ref:
                images.append(rel.target_ref)
        return images

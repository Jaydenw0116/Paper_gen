import re
from io import BytesIO
from docx import Document
from docxcompose.composer import Composer
from typing import List


class DocumentComposer:
    """
    简化的文档合成器，模仿app.py的思路
    """

    @staticmethod
    def renumber_question(doc_bytes: bytes, new_number: int) -> bytes:
        """
        重编号问题，只替换第一个文本元素中的数字
        """
        try:
            doc = Document(BytesIO(doc_bytes))
            found = False
            
            for child in doc.element.body:
                if child.tag.endswith("p") or child.tag.endswith("tbl"):
                    
                    def traverse_and_replace(node, inside_drawing=False):
                        nonlocal found
                        if found:
                            return
                        
                        tag = node.tag.lower() if hasattr(node, 'tag') else ''
                        is_drawing = (
                            inside_drawing
                            or 'drawing' in tag
                            or 'shape' in tag
                            or 'alternatecontent' in tag
                        )
                        
                        if tag.endswith('t') and node.text and node.text.strip() and not is_drawing:
                            if re.match(r"^\s*\d+[\.．、]", node.text):
                                # 替换题号中的数字部分
                                node.text = re.sub(r"^\s*\d+", str(new_number), node.text, count=1)
                                found = True
                                return
                            found = True
                            return
                        
                        if hasattr(node, '__iter__'):
                            for c in node:
                                traverse_and_replace(c, is_drawing)
                    
                    traverse_and_replace(child)
                if found:
                    break
            
            output = BytesIO()
            doc.save(output)
            return output.getvalue()
        except Exception:
            return doc_bytes

    @staticmethod
    def compose_documents(template_bytes: bytes, question_bytes_list: List[bytes]) -> bytes:
        """
        合并多个问题文档到模板文档中
        """
        template_doc = Document(BytesIO(template_bytes))
        composer = Composer(template_doc)

        for q_idx, q_bytes in enumerate(question_bytes_list, start=1):
            renumbered_bytes = DocumentComposer.renumber_question(q_bytes, q_idx)
            question_doc = Document(BytesIO(renumbered_bytes))
            composer.append(question_doc)

        output = BytesIO()
        template_doc.save(output)
        return output.getvalue()

    @staticmethod
    def create_empty_template() -> bytes:
        """创建空模板文档"""
        doc = Document()
        output = BytesIO()
        doc.save(output)
        return output.getvalue()

    @staticmethod
    def load_template(template_path: str) -> bytes:
        """加载模板文档"""
        with open(template_path, 'rb') as f:
            return f.read()

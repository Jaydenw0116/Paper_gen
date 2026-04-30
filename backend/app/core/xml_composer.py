import re
from io import BytesIO
from docx import Document
from docxcompose.composer import Composer
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from typing import List, Dict
import copy

class DocumentComposer:
    QUESTION_NUMBER_REGEX = re.compile(r'^\s*\d+[\.．、]')
    QUESTION_LABEL_REGEX = re.compile(r'^\s*第\s*\d+\s*题')

    @staticmethod
    def renumber_question(doc_bytes: bytes, new_number: int) -> bytes:
        doc = Document(BytesIO(doc_bytes))
        number_replaced = False
        first_paragraph_found = False
        
        for element in doc.element.body:
            if element.tag.endswith('p'):
                if not first_paragraph_found:
                    if DocumentComposer._renumber_paragraph(element, new_number):
                        number_replaced = True
                    first_paragraph_found = True
                else:
                    DocumentComposer._clean_extra_numbers(element)
            elif element.tag.endswith('tbl'):
                if not first_paragraph_found:
                    if DocumentComposer._renumber_table(element, new_number):
                        number_replaced = True
                    first_paragraph_found = True
                else:
                    DocumentComposer._clean_table_numbers(element)
        
        if not number_replaced:
            first_paragraph = doc.paragraphs[0] if doc.paragraphs else doc.add_paragraph()
            first_paragraph.text = f"{new_number}. {first_paragraph.text}"

        output = BytesIO()
        doc.save(output)
        return output.getvalue()

    @staticmethod
    def _renumber_paragraph(paragraph_element, new_number: int):
        # 获取段落中的所有文本元素
        text_elements = []
        for child in paragraph_element.iter():
            if child.tag.endswith('t') and child.text:
                text_elements.append(child)
        
        if not text_elements:
            return False
        
        # 获取第一个文本元素的内容
        first_text = text_elements[0].text
        
        # 检查是否匹配题号模式
        match = DocumentComposer.QUESTION_NUMBER_REGEX.match(first_text)
        if match:
            # 替换整个题号部分
            text_elements[0].text = f"{new_number}." + first_text[len(match.group()):]
            return True
        
        # 尝试匹配"第X题"模式
        match = DocumentComposer.QUESTION_LABEL_REGEX.match(first_text)
        if match:
            text_elements[0].text = f"{new_number}." + first_text[len(match.group()):]
            return True
        
        return False

    @staticmethod
    def _clean_extra_numbers(paragraph_element):
        # 清理段落中除了开头以外的题号
        number_pattern = re.compile(r'(?<![\d\.])\d+[\.．、](?!\d)')
        
        for child in paragraph_element.iter():
            if child.tag.endswith('t') and child.text:
                # 替换掉所有题号模式，但保留内容
                child.text = number_pattern.sub('', child.text)

    @staticmethod
    def _renumber_table(table_element, new_number: int):
        for child in table_element.iter():
            if child.tag.endswith('t') and child.text:
                match = DocumentComposer.QUESTION_NUMBER_REGEX.match(child.text)
                if match:
                    child.text = f"{new_number}." + child.text[len(match.group()):]
                    return True
                
                match = DocumentComposer.QUESTION_LABEL_REGEX.match(child.text)
                if match:
                    child.text = f"{new_number}." + child.text[len(match.group()):]
                    return True
        return False

    @staticmethod
    def _clean_table_numbers(table_element):
        number_pattern = re.compile(r'(?<![\d\.])\d+[\.．、](?!\d)')
        for child in table_element.iter():
            if child.tag.endswith('t') and child.text:
                child.text = number_pattern.sub('', child.text)

    @staticmethod
    def compose_documents(template_bytes: bytes, question_bytes_list: List[bytes]) -> bytes:
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
        doc = Document()
        output = BytesIO()
        doc.save(output)
        return output.getvalue()

    @staticmethod
    def load_template(template_path: str) -> bytes:
        with open(template_path, 'rb') as f:
            return f.read()

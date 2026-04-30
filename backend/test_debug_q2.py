import subprocess
import json
import zipfile
import re

# 获取题库中的题号2
result = subprocess.run(
    ['curl', '-s', 'http://localhost:8000/api/bank'],
    capture_output=True, text=True
)
bank_data = json.loads(result.stdout)

q2_data = None
for q in bank_data:
    if q['original_no'] == '2.':
        q2_data = q
        break

if q2_data:
    q2_id = q2_data['id']
    print(f"题号2的ID: {q2_id}")
    
    # 直接测试renumber_question功能
    import sys
    sys.path.insert(0, '/Users/wuhuangjian/Desktop/Paper_gen/backend')
    
    from app.core.cache import cache_manager
    import ast
    
    # 获取题库数据
    bank_bytes = cache_manager.get_docx_bytes("question_bank")
    bank = ast.literal_eval(bank_bytes.decode('utf-8'))
    
    # 获取题号2的原始文档字节
    q2_bytes = bank["answers"][q2_id]["question"]
    
    from app.core.xml_composer import DocumentComposer
    
    # 测试重编号
    renumbered_bytes = DocumentComposer.renumber_question(q2_bytes, 2)
    
    # 检查重编号后的内容
    from io import BytesIO
    from docx import Document
    
    doc = Document(BytesIO(renumbered_bytes))
    print("\n题号2重编号后的内容:")
    for para in doc.paragraphs:
        print(f"段落: '{para.text}'")
    
    # 检查XML内容
    output = BytesIO()
    doc.save(output)
    output.seek(0)
    
    with zipfile.ZipFile(BytesIO(output.read()), 'r') as z:
        xml_content = z.read('word/document.xml').decode('utf-8')
        
    # 提取所有文本内容
    text_elements = re.findall(r'<w:t>([^<]*)</w:t>', xml_content)
    print("\nXML中的文本元素:")
    for i, text in enumerate(text_elements):
        print(f"{i}: '{text}'")
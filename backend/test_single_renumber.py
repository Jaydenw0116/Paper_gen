import sys
import json
import subprocess
import zipfile
import re
from io import BytesIO
from docx import Document

# Upload files
upload_result = subprocess.run(
    ['curl', '-X', 'POST', 'http://localhost:8000/api/upload',
     '-F', 'question_file=@../4C 10 test.docx',
     '-F', 'answer_file=@../4C 10 test sol.docx'],
    capture_output=True, text=True
)

upload_data = json.loads(upload_result.stdout)
first_q = upload_data['questions'][0]
print(f"第一个问题: {first_q['original_no']}")
print(f"预览文本: {first_q['preview_text'][:100]}")

# Get the question bytes from cache
question_id = first_q['id']
session_id = upload_data['session_id']

# Save a test question
subprocess.run([
    'curl', '-s', f"http://localhost:8000/api/download-question/{session_id}/{question_id}",
    '-o', '/tmp/first_question.docx'
])

# Check the content
with zipfile.ZipFile('/tmp/first_question.docx', 'r') as z:
    xml_content = z.read('word/document.xml').decode('utf-8')

matches = re.findall(r'<w:t>([^<]+)</w:t>', xml_content)
number_like = [m for m in matches if re.match(r'^\s*\d+[\.．、]', m)]
print(f"\n问题块中的题号: {number_like}")

# Test renumbering
from core.xml_composer import DocumentComposer

with open('/tmp/first_question.docx', 'rb') as f:
    q_bytes = f.read()

renumbered_bytes = DocumentComposer.renumber_question(q_bytes, 1)

with zipfile.ZipFile(BytesIO(renumbered_bytes), 'r') as z:
    xml_content = z.read('word/document.xml').decode('utf-8')

matches = re.findall(r'<w:t>([^<]+)</w:t>', xml_content)
number_like = [m for m in matches if re.match(r'^\s*\d+[\.．、]', m)]
print(f"重新编号后的题号: {number_like}")

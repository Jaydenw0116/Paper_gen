import subprocess
import json
import zipfile
import re

# Upload
upload_result = subprocess.run(
    ['curl', '-s', '-X', 'POST', 'http://localhost:8000/api/upload',
     '-F', 'question_file=@../4C 10 test.docx',
     '-F', 'answer_file=@../4C 10 test sol.docx'],
    capture_output=True, text=True
)
upload_data = json.loads(upload_result.stdout)
question_ids = [q['id'] for q in upload_data['questions']]

# Upload to bank
subprocess.run([
    'curl', '-s', '-X', 'POST', 'http://localhost:8000/api/upload-to-bank',
    '-H', 'Content-Type: application/json',
    '-d', json.dumps({'session_id': upload_data['session_id'], 'question_ids': question_ids})
])

# Compose
compose_result = subprocess.run([
    'curl', '-s', '-X', 'POST', 'http://localhost:8000/api/compose',
    '-H', 'Content-Type: application/json',
    '-d', json.dumps({'question_ids': question_ids})
], capture_output=True, text=True)
compose_data = json.loads(compose_result.stdout)
compose_session_id = compose_data['session_id']

# Download paper
subprocess.run([
    'curl', '-s', '-o', '/tmp/test_paper_final.docx',
    f"http://localhost:8000/api/download/{compose_session_id}/paper"
])

# Check content
with zipfile.ZipFile('/tmp/test_paper_final.docx', 'r') as z:
    xml_content = z.read('word/document.xml').decode('utf-8')

# Extract numbers
numbers = re.findall(r'<w:t>(\d+)\.</w:t>', xml_content)
print(f"试卷题号序列: {numbers}")

# Verify
expected = [str(i) for i in range(1, len(numbers)+1)]
if numbers == expected:
    print("✓ 试卷题号正确，从1开始依次增加")
else:
    print("✗ 试卷题号不正确")
    print(f"期望: {expected}")
    print(f"实际: {numbers}")

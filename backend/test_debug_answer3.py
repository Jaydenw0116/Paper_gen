import sys
import json
import subprocess

# 上传问题文件和答案文件
upload_result = subprocess.run(
    ['curl', '-X', 'POST', 'http://localhost:8000/api/upload',
     '-F', 'question_file=@../4C 10 test.docx',
     '-F', 'answer_file=@../4C 10 test sol.docx'],
    capture_output=True, text=True
)

upload_data = json.loads(upload_result.stdout)
print(f"问题文档解析出 {len(upload_data['questions'])} 个问题")

# 检查每个问题是否有对应的答案题号
for i, q in enumerate(upload_data['questions']):
    print(f"\n问题 {i+1}:")
    print(f"  题号: {q['original_no']}")
    print(f"  ID: {q['id']}")
    # 检查是否有 answer_id
    if 'answer_id' in q:
        print(f"  answer_id: {q['answer_id']}")
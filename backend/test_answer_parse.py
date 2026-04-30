import sys
import json
import subprocess
import zipfile
import re

# Upload files
upload_result = subprocess.run(
    ['curl', '-X', 'POST', 'http://localhost:8000/api/upload',
     '-F', 'question_file=@../4C 10 test.docx',
     '-F', 'answer_file=@../4C 10 test sol.docx'],
    capture_output=True, text=True
)

upload_data = json.loads(upload_result.stdout)
print(f"上传了 {len(upload_data['questions'])} 个问题")

# 打印每个问题的题号和预览
for i, q in enumerate(upload_data['questions']):
    print(f"\n问题 {i+1}:")
    print(f"  原始题号: {q['original_no']}")
    print(f"  预览文本: {q['preview_text'][:80]}")
    
    # 检查是否包含答案文档中的题号格式
    if '3.' in q['preview_text']:
        print("  *** 包含题号 3 ***")
    if '10.' in q['preview_text']:
        print("  *** 包含题号 10 ***")
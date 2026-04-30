import sys
import json
import subprocess

# 只上传答案文件来检查解析结果
upload_result = subprocess.run(
    ['curl', '-X', 'POST', 'http://localhost:8000/api/upload',
     '-F', 'answer_file=@../4C 10 test sol.docx'],
    capture_output=True, text=True
)

print(f"响应: {upload_result.stdout}")
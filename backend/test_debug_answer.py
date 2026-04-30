import sys
import json
import subprocess

# 只上传答案文件来检查解析结果
upload_result = subprocess.run(
    ['curl', '-X', 'POST', 'http://localhost:8000/api/upload',
     '-F', 'answer_file=@../4C 10 test sol.docx'],
    capture_output=True, text=True
)

upload_data = json.loads(upload_result.stdout)
print(f"解析出 {len(upload_data['questions'])} 个问题")

# 打印每个问题的详细信息
for i, q in enumerate(upload_data['questions']):
    print(f"\n问题 {i+1}:")
    print(f"  原始题号: {repr(q['original_no'])}")
    print(f"  预览文本: {repr(q['preview_text'][:100])}")
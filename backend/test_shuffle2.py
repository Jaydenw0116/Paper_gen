import subprocess
import json
import random

# 上传文件
result = subprocess.run(
    ['curl', '-s', '-X', 'POST', 'http://localhost:8000/api/upload',
     '-F', 'question_file=@../OSM_ChapterTest_4B08_Lite_c.docx',
     '-F', 'answer_file=@../OSM_ChapterTest_4B08_Lite_sol_c.docx'],
    capture_output=True, text=True
)
upload_data = json.loads(result.stdout)
session_id = upload_data['session_id']
question_count = len(upload_data['questions'])

print(f"上传成功，解析出 {question_count} 个问题")
print(f"原始题号: {[q['original_no'] for q in upload_data['questions']]}")

# 打乱顺序
shuffled_indices = list(range(question_count))
random.shuffle(shuffled_indices)
print(f"\n打乱后的索引: {shuffled_indices}")

# 创建打乱后的题目列表
questions_to_compose = []
for idx in shuffled_indices:
    q = upload_data['questions'][idx]
    questions_to_compose.append({
        'id': q['id'],
        'order': len(questions_to_compose) + 1
    })

# 组卷生成
compose_data = json.dumps({
    'session_id': session_id,
    'questions': questions_to_compose
})

result = subprocess.run(
    ['curl', '-s', '-X', 'POST', 'http://localhost:8000/api/compose',
     '-H', 'Content-Type: application/json',
     '-d', compose_data],
    capture_output=True, text=True
)
print(f"组卷响应: {result.stdout}")
if result.stderr:
    print(f"组卷错误: {result.stderr}")
import subprocess
import json
import random
import zipfile
import re

# 上传文件
result = subprocess.run(
    ['curl', '-s', '-X', 'POST', 'http://localhost:8000/api/upload',
     '-F', 'question_file=@../OSM_ChapterTest_4B08_Lite_c.docx',
     '-F', 'answer_file=@../OSM_ChapterTest_4B08_Lite_sol_c.docx'],
    capture_output=True, text=True
)
upload_data = json.loads(result.stdout)
session_id = upload_data['session_id']
questions = upload_data['questions']
question_count = len(questions)

print(f"上传成功，解析出 {question_count} 个问题")
print(f"原始题号: {[q['original_no'] for q in questions]}")

# 获取所有问题ID
question_ids = [q['id'] for q in questions]

# 上传到题库（使用session_id和question_ids参数）
upload_to_bank_data = json.dumps({'session_id': session_id, 'question_ids': question_ids})
result = subprocess.run(
    ['curl', '-s', '-X', 'POST', 'http://localhost:8000/api/upload-to-bank',
     '-H', 'Content-Type: application/json',
     '-d', upload_to_bank_data],
    capture_output=True, text=True
)
print(f"\n上传到题库: {result.stdout}")

# 打乱顺序
random.shuffle(question_ids)
print(f"\n打乱后的ID顺序: {question_ids}")

# 组卷生成
compose_data = json.dumps({
    'question_ids': question_ids
})

result = subprocess.run(
    ['curl', '-s', '-X', 'POST', 'http://localhost:8000/api/compose',
     '-H', 'Content-Type: application/json',
     '-d', compose_data],
    capture_output=True, text=True
)
print(f"组卷响应: {result.stdout}")

try:
    compose_result = json.loads(result.stdout)
    if 'paper_id' in compose_result:
        paper_id = compose_result['paper_id']
        print(f"\n组卷成功，paper_id: {paper_id}")
        
        # 下载生成的试卷和答案
        subprocess.run(['curl', '-s', '-o', '../generated_paper.docx',
                        f'http://localhost:8000/api/download-paper/{paper_id}'])
        subprocess.run(['curl', '-s', '-o', '../generated_answer.docx',
                        f'http://localhost:8000/api/download-answer/{paper_id}'])
        
        print("\n=== 检查生成的试卷文件 ===")
        with zipfile.ZipFile('../generated_paper.docx', 'r') as z:
            xml_content = z.read('word/document.xml').decode('utf-8')
        
        # 提取题号
        paper_numbers = []
        for match in re.finditer(r'<w:t>(\d+[\.．、])</w:t>', xml_content):
            paper_numbers.append(match.group(1))
        
        # 去重并按出现顺序排列
        unique_paper_numbers = []
        seen = set()
        for num in paper_numbers:
            if num not in seen:
                seen.add(num)
                unique_paper_numbers.append(num)
        
        print(f"试卷题号: {unique_paper_numbers}")
        
        # 检查是否连续
        is_continuous = True
        for i in range(len(unique_paper_numbers)):
            expected = f"{i+1}."
            if unique_paper_numbers[i] != expected:
                is_continuous = False
                print(f"  发现不连续: 期望 {expected}, 实际 {unique_paper_numbers[i]}")
                break
        
        if is_continuous:
            print("  ✓ 试卷题号连续")
        
        print("\n=== 检查生成的答案文件 ===")
        with zipfile.ZipFile('../generated_answer.docx', 'r') as z:
            xml_content = z.read('word/document.xml').decode('utf-8')
        
        # 提取题号
        answer_numbers = []
        for match in re.finditer(r'<w:t>(\d+[\.．、])</w:t>', xml_content):
            answer_numbers.append(match.group(1))
        
        # 去重并按出现顺序排列
        unique_answer_numbers = []
        seen = set()
        for num in answer_numbers:
            if num not in seen:
                seen.add(num)
                unique_answer_numbers.append(num)
        
        print(f"答案题号: {unique_answer_numbers}")
        
        # 检查是否连续
        is_continuous = True
        for i in range(len(unique_answer_numbers)):
            expected = f"{i+1}."
            if unique_answer_numbers[i] != expected:
                is_continuous = False
                print(f"  发现不连续: 期望 {expected}, 实际 {unique_answer_numbers[i]}")
                break
        
        if is_continuous:
            print("  ✓ 答案题号连续")
        
        # 检查试卷和答案题号是否一致
        if unique_paper_numbers == unique_answer_numbers:
            print("\n✓ 试卷和答案题号一致")
        else:
            print("\n✗ 试卷和答案题号不一致")
            print(f"  试卷题号: {unique_paper_numbers}")
            print(f"  答案题号: {unique_answer_numbers}")
            
except json.JSONDecodeError:
    print(f"解析响应失败: {result.stdout}")
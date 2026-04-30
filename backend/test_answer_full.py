import zipfile
import re

with zipfile.ZipFile('../4C 10 test sol.docx', 'r') as z:
    xml_content = z.read('word/document.xml').decode('utf-8')

# 分割文档内容
lines = xml_content.split('<w:p')
print(f"总段落数: {len(lines)-1}")

print("\n===== 所有包含题号的段落 =====")
question_paragraphs = []
for i, part in enumerate(lines[1:], 1):
    text_matches = re.findall(r'<w:t>([^<]+)</w:t>', part)
    if text_matches:
        full_text = ''.join(text_matches)
        # 检查是否包含题号模式
        if re.search(r'^\s*\d+[\.．、]', full_text):
            question_paragraphs.append((i, full_text))
            print(f"\n段落 {i}:")
            print(f"  文本: {repr(full_text[:100])}")

print(f"\n\n===== 查看题号1和3之间的段落 =====")
for i in range(question_paragraphs[0][0]+1, question_paragraphs[1][0]):
    if i < len(lines):
        part = lines[i]
        text_matches = re.findall(r'<w:t>([^<]+)</w:t>', part)
        if text_matches:
            full_text = ''.join(text_matches)
            if full_text.strip():
                print(f"段落 {i}: {repr(full_text)}")
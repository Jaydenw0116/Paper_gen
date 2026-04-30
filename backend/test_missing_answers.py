import zipfile
import re

with zipfile.ZipFile('../4C 10 test sol.docx', 'r') as z:
    xml_content = z.read('word/document.xml').decode('utf-8')

# 分割文档内容，看看所有段落
lines = xml_content.split('<w:p')
print(f"总段落数: {len(lines)-1}")

print("\n===== 搜索缺少的题号 =====")
for i, part in enumerate(lines[1:], 1):
    text_matches = re.findall(r'<w:t>([^<]+)</w:t>', part)
    if text_matches:
        full_text = ''.join(text_matches)
        # 检查是否包含我们需要找的题号
        if '2.' in full_text or '4.' in full_text or '6.' in full_text or '10.' in full_text:
            print(f"\n段落 {i}:")
            print(f"  文本: {repr(full_text[:150])}")
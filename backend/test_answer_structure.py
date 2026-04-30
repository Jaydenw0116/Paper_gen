import zipfile
import re

with zipfile.ZipFile('../4C 10 test sol.docx', 'r') as z:
    xml_content = z.read('word/document.xml').decode('utf-8')

# 分割文档内容，看看题号的位置
lines = xml_content.split('<w:p')
print(f"总段落数: {len(lines)-1}")

print("\n===== 包含数字的段落 =====")
for i, part in enumerate(lines[1:], 1):
    # 提取文本内容
    text_matches = re.findall(r'<w:t>([^<]+)</w:t>', part)
    if text_matches:
        full_text = ''.join(text_matches)
        # 检查是否包含题号模式
        if re.search(r'\d+[\.．、]', full_text):
            print(f"\n段落 {i}:")
            print(f"  文本: {repr(full_text[:100])}")
            
            # 检查是否匹配题号正则
            for t in text_matches:
                if re.match(r'^\s*\d+[\.．、](?!\d)', t):
                    print(f"    匹配题号: {repr(t)}")
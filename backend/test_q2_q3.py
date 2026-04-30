import zipfile
import re

with zipfile.ZipFile('../OSM_ChapterTest_4B08_Lite_c.docx', 'r') as z:
    xml_content = z.read('word/document.xml').decode('utf-8')

# 分割文档内容
lines = xml_content.split('<w:p')
print(f"总段落数: {len(lines)-1}")

print("\n===== 搜索题号2和3附近的段落 =====")
for i in range(1, len(lines)):
    part = lines[i]
    text_matches = re.findall(r'<w:t>([^<]+)</w:t>', part)
    if text_matches:
        full_text = ''.join(text_matches)
        # 检查是否包含题号2或3
        if '2.' in full_text or '3.' in full_text:
            print(f"\n段落 {i}:")
            print(f"  文本: {repr(full_text)}")
            
# 查看第二题和第三题之间的详细内容
print("\n===== 详细查看题号2之后的段落 =====")
found_q2 = False
count = 0
for i in range(1, len(lines)):
    part = lines[i]
    text_matches = re.findall(r'<w:t>([^<]+)</w:t>', part)
    if text_matches:
        full_text = ''.join(text_matches)
        if '2.' in full_text:
            found_q2 = True
            print(f"\n段落 {i} (找到题号2):")
            print(f"  文本: {repr(full_text[:200])}")
            count = 0
        elif found_q2 and count < 30:
            count += 1
            if full_text.strip():
                print(f"段落 {i}: {repr(full_text[:100])}")
                # 检查是否有题号3
                if '3.' in full_text:
                    print("    -> 发现题号3!")
                    break
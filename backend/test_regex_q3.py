import re

# 当前的正则表达式
QUESTION_NUMBER_REGEX = re.compile(r'^\s*\d+[\.．、](?!\d+$)|^\s*\d+[\.．、]$')

# 测试各种题号格式
test_cases = [
    '1.',
    '2.化簡log5',
    '3.(a)根據0.5x',
    '3.',
    '  4.',
    '5(b)',
    '6、测试'
]

print("测试正则表达式匹配：")
for tc in test_cases:
    match = QUESTION_NUMBER_REGEX.match(tc)
    print(f"  '{tc}' -> {match.group() if match else None}")

# 检查特殊情况
print("\n检查特殊情况：")
text = '3.(a)根據0.5x的圖像，在圖中描繪y0.5x的草圖。(3分)'
match = QUESTION_NUMBER_REGEX.match(text)
if match:
    print(f"  匹配到: {repr(match.group())}")
    print(f"  匹配长度: {len(match.group())}")
    print(f"  去掉题号后的内容: {repr(text[len(match.group()):])}")
import re

test_cases = [
    '3.', '10.', '1.50=', '5.∵圖像', '7.x= 3', '8.x', '9.4xxx', 
    '11.A', '12.C', '13.D', '14.A', '15.cos',
    '0.5', '36.9', '143.1', '0.1', '18.435'
]

pattern = re.compile(r'^\s*\d+[\.．、](?!\d)|^\s*\d+[\.．、](?=\s)')

print('测试正则表达式:')
for tc in test_cases:
    match = pattern.match(tc)
    result = '✓ 匹配' if match else '✗ 不匹配'
    print(f'{tc:10} {result}')

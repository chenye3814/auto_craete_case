import re

qq = '1826755263'
print(re.match(r'[1-9]\d{4,11}', qq))
# print(qq)

qq = '1826755263'
print(re.fullmatch(r'[1-9]\d{4,11}', qq))
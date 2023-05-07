import re
import sys

'''跨行公式, 替代成了单行公式符号'''
if len(sys.argv) < 2:
    print("Usage: python script_name.py <filename>")
    sys.exit(1)

filename = sys.argv[1]

with open(filename, "rb") as f:
    text = f.read()
    text = str(text, 'utf-8')

# replace math formulas surrounded by continuous $$ with \[\]
text = re.sub(r"\$\$(.*?)\$\$", r"\\\[\1\\\]", text, flags=re.DOTALL)

# replace math formulas surrounded by single $ with \(\)
text = re.sub(r"\$(.*?)\$", r"\\\(\1\\\)", text, flags = re.DOTALL)

with open(filename, "wb") as f:
    text = bytes(text, 'utf-8')
    f.write(text)

print(f"File '{filename}' has been updated.")


import sys, os

def convert_punctuation_cn_to_en(text: str) -> str:
    cn_to_en_punctuation_map = {
        "。": ". ",
        "，": ", ",
        "、": ", ",
        "“": "\"",
        "”": "\"",
        "‘": "'",
        "’": "'",
        "！": "! ",
        "？": "? ",
        "【": "[",
        "】": "]",
        "（": "(",
        "）": ")",
        "；": "; ",
        "：": ": ",
        "——": "_",
        "……": "^"
    }

    for cn_punc, en_punc in cn_to_en_punctuation_map.items():
        text = text.replace(cn_punc, en_punc)
    return text.strip()


if __name__ == "__main__":
    if len(sys.argv)>1:
        # 命令行参数输入目标文件夹
        path = sys.argv[1]

        with open(path, 'rb') as f:
            text = f.read()
            text = str(text, 'utf-8')
    else:
        path='C:\\Users\\y\'j\'w\\Desktop\\tmp1.md'
        # 从stdin读取
        text = ''
        while True:
            byte = sys.stdin.read(1)
            if not byte:
                break
            else:
                text += byte

    text = convert_punctuation_cn_to_en(text)

    with open(path, 'wb') as f:
        text = bytes(text, 'utf-8')
        f.write(text)

    print(f"File '{path}'has been updated!")

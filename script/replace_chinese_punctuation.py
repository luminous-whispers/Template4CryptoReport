import sys, os

def convert_punctuation_cn_to_en(text: str) -> str:
    cn_to_en_punctuation_map = {
        "。": ". ",
        "，": ", ",
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
    else:
        # 硬编码目标文件夹，请自行修改
        path = "D:\yjw\course\Cryptography\CryptoLab\code\c8-ECC"
    with open(path, 'rb') as f:
        text = f.read()
        text = str(text, 'utf-8')

    text = convert_punctuation_cn_to_en(text)

    with open(path, 'wb') as f:
        text = bytes(text, 'utf-8')
        f.write(text)

    print(f"File '{path}'has been updated!")

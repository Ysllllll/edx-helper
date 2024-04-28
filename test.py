import re
import json
import requests
from bs4 import BeautifulSoup

# zh_url = "https://courses.edx.org/courses/course-v1:MITx+6.002.1x+2T2019/xblock/block-v1:MITx+6.002.1x+2T2019+type@video+block@d8b7197ab92044f189728ed61b968781/handler/transcript/translation/zh"
# en_url = "https://courses.edx.org/courses/course-v1:MITx+6.002.1x+2T2019/xblock/block-v1:MITx+6.002.1x+2T2019+type@video+block@d8b7197ab92044f189728ed61b968781/handler/transcript/translation/en"


# # # 发送GET请求
# # # response = requests.get(url)


# with open("cookies.txt", "r") as f:
#     cookies = f.read()
#     cookies_list = cookies.split(";")
#     cookies_list = [cook.strip() for cook in cookies_list]
#     cookies_dict = {}

#     for cook in cookies_list:
#         ret = cook.split("=")
#         cookies_dict[ret[0]] = ret[1]
#     headers = {
#         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
#         "Accept-Language": "en-US,en;q=0.9",
#         "Content-Type": "application/json",  # 如果发送JSON数据，这个头部很常见
#     }
#     zh_response = requests.get(zh_url, headers=headers, cookies=cookies_dict)
#     en_response = requests.get(en_url, headers=headers, cookies=cookies_dict)

#     import pdb

#     pdb.set_trace()
#     # 检查请求是否成功（状态码200表示成功）
#     if zh_response.status_code == 200 and en_response.status_code == 200:

#         zh_text = eval(zh_response.text)
#         en_text = eval(en_response.text)
#         with open("zh_text.json", "w", encoding="utf-8") as f:
#             json.dump(zh_text, f, ensure_ascii=False)
#         with open("en_text.json", "w", encoding="utf-8") as f:
#             json.dump(en_text, f, ensure_ascii=False)

#         # 使用BeautifulSoup解析网页内容
#         # 这里可以根据需要解析具体的网页内容，例如查找特定的标签、类名或属性
#         # 以下仅为示例，具体解析逻辑需根据目标网页的实际结构来定
#         # print(soup.find('div', class_='your-target-class').get_text())
#     else:
#         print("Failed to retrieve the content. Status code:", response.status_code)


with open("zh_text.json", "r", encoding="utf-8") as f:
    zh_text = json.load(f)
with open("en_text.json", "r", encoding="utf-8") as f:
    en_text = json.load(f)
# import pdb

# pdb.set_trace()


def merge_zh_en_subtitle(zh_text, en_text):
    zh_text_new = {"start": [], "end": [], "text": []}
    for start, end, text in zip(zh_text["start"], zh_text["end"], zh_text["text"]):
        if re.findall(r"字幕组", text):
            continue
        else:
            zh_text_new["start"].append(start)
            zh_text_new["end"].append(end)
            zh_text_new["text"].append(text)
    zh_text = zh_text_new

    ret = {"start": [], "end": [], "zh": [], "en": []}
    zh_len = len(zh_text["start"])
    en_len = len(en_text["start"])

    zh_idx = 0
    en_idx = 0

    while zh_idx < zh_len and en_idx < en_len:
        if (
            zh_text["start"][zh_idx] == en_text["start"][en_idx]
            and zh_text["end"][zh_idx] == en_text["end"][en_idx]
        ):
            ret["start"].append(zh_text["start"][zh_idx])
            ret["end"].append(zh_text["end"][zh_idx])
            ret["zh"].append(zh_text["text"][zh_idx])
            ret["en"].append(en_text["text"][en_idx])
            zh_idx += 1
            en_idx += 1
        elif (
            zh_text["start"][zh_idx] < en_text["start"][en_idx]
            and zh_text["end"][zh_idx] < en_text["end"][en_idx]
        ):
            ret["start"].append(zh_text["start"][zh_idx])
            ret["end"].append(zh_text["end"][zh_idx])
            ret["zh"].append(zh_text["text"][zh_idx])
            ret["en"].append("")
            zh_idx += 1
        else:
            ret["start"].append(en_text["start"][en_idx])
            ret["end"].append(en_text["end"][en_idx])
            ret["zh"].append("")
            ret["en"].append(en_text["text"][en_idx])
            en_idx += 1

    while zh_idx < zh_len:
        ret["start"].append(zh_text["start"][zh_idx])
        ret["end"].append(zh_text["end"][zh_idx])
        ret["zh"].append(zh_text["text"][zh_idx])
        ret["en"].append("")
        zh_idx += 1

    while en_idx < en_len:
        ret["start"].append(en_text["start"][en_idx])
        ret["end"].append(en_text["end"][en_idx])
        ret["zh"].append("")
        ret["en"].append(en_text["text"][en_idx])
        en_idx += 1
    return ret


from datetime import timedelta, datetime


def edx_json2srt(o):
    """
    Transform the dict 'o' into the srt subtitles format
    """
    if o == {}:
        return ""

    base_time = datetime(1, 1, 1)
    output = []

    def get_time_str(s, e):
        s = base_time + timedelta(seconds=s / 1000.0)
        e = base_time + timedelta(seconds=e / 1000.0)
        return "%02d:%02d:%02d,%03d --> %02d:%02d:%02d,%03d" % (
            s.hour,
            s.minute,
            s.second,
            s.microsecond / 1000,
            e.hour,
            e.minute,
            e.second,
            e.microsecond / 1000,
        )

    first_time = o["end"][0] // 10
    time_range = get_time_str(0, first_time)
    output.append(f"{len(output) + 1}\n{time_range}\n字幕制作/整理：Edx")
    change_flag = True
    for i, (s, e, zh, en) in enumerate(zip(o["start"], o["end"], o["zh"], o["en"])):
        zhl = zh.lower()
        enl = en.lower()
        if (
            (zhl == "null" and enl == "none")
            or (zhl == "none" and enl == "none")
            or (zhl == "null" and enl == "null")
            or (zhl == "none" and enl == "null")
        ):
            continue

        if change_flag:
            time_range = get_time_str(o["end"][0] // 10, e)
            change_flag = False
        else:
            time_range = get_time_str(s, e)

        zh = re.sub("&#39;", "'", zh)
        en = re.sub("&#39;", "'", en)

        out_str = None
        if zh and en:
            out_str = f"{len(output) + 1}\n{time_range}\n{zh}\n{en}"
        elif zh:
            out_str = f"{len(output) + 1}\n{time_range}\n{zh}"
        elif en:
            out_str = f"{len(output) + 1}\n{time_range}\n{en}"
        if out_str:
            output.append(out_str)

    return "\n\n".join(output)


ret = merge_zh_en_subtitle(zh_text, en_text)
x = edx_json2srt(ret)
with open("test.srt", "w", encoding="UTF-8") as f:
    f.write(x)
    f.flush()

    import pdb

    pdb.set_trace()
    print(x)

import json
from xml.etree.ElementTree import indent

from zhipuai import ZhipuAI
import re

# client = ZhipuAI(api_key="53c8378d900c4f31bdbe6d564b33c0f8.Ta4Z1YRszdFJfhL3")  # 请填写您自己的APIKey

# Please install OpenAI SDK first: `pip3 install openai`

from openai import OpenAI

client = OpenAI(api_key="sk-aae01ef2678e4200a51c8a3f8b9c9313", base_url="https://api.deepseek.com")



def get_events(text):
    '''
    按文本提取事件名称， 并返回事件列表。
    '''

    pattern = r'\d+\.\s*(.+?)\n'
    events = re.findall(pattern, text, flags=re.DOTALL)
    # print('events: ', events)
    return events


def get_event_text(txt):
    '''
    根据文本内容，提取事件，返回事件列表文本。
    '''
    prompt = '''根据文本内容，提取事件名称，如果事件有时间就把事件加上。

以下是文本内容：
{}
'''
    stream = False
    response = client.chat.completions.create(
        model="deepseek-chat",  # 填写需要调用的模型名称
        messages=[
            {"role": "user", "content": prompt.format(txt)},
        ],
        # 是否
        stream=stream,
    )

    content = response.choices[0].message.content
    return content


def get_person_text(person_name):
    '''
    根据人物名称获取人物经理。
    '''
    prompt = "{}的履历".format(person_name)
    stream = False
    response = client.chat.completions.create(
        model="deepseek-chat",  # 填写需要调用的模型名称
        messages=[
            {"role": "system", "content": "你是一个信息处理专家，你的任务是为用户提供专业、准确的信息。"},
            {"role": "user", "content": prompt},
        ],
        # 是否
        stream=stream,
    )
    content = response.choices[0].message.content
    return content


def get_event_detail(person_name, event_name):
    '''
    根据事件名称获取。
    '''
    prompt = """根据事件和事件，提供事件的详细经过。

以下是事件名称和事件:
{}: {}""".format(person_name, event_name)

    stream = False
    try:
        response = client.chat.completions.create(
            model="deepseek-chat",  # 填写需要调用的模型名称
            messages=[
                {"role": "system", "content": "你是一个信息处理专家，你的任务是为用户提供专业、准确的信息。"},
                {"role": "user", "content": prompt},
            ],
            # 是否
            stream=stream,
        )
        content = response.choices[0].message.content
    except Exception as e:
        content = e.response.json()['error']['message']
    return content


if __name__ == '__main__':
    person_name = '石破茂'
    txt = get_person_text(person_name)


    event_text = get_event_text(txt)
    events = get_events(event_text)
    person_json = {person_name: []}
    for event in events:
        event_detail = get_event_detail(person_name, event)
        print("event_detail: ", event_detail)
        person_json[person_name].append({event: event_detail})
    with open('{}.json'.format(person_name), 'w', encoding='utf-8') as f:
        json.dump(person_json, f, ensure_ascii=False, indent=4)

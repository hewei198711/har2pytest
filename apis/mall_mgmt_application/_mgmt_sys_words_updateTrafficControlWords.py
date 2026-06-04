import os

from util.client import client

data = {
    "id": 0,  # 主键id
    "words": "",  # 提示语
    "wordsType": 0,  # 类型 0：不可发货 1：可发货但影响配送时效
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_sys_words_updateTrafficControlWords(data=data, headers=headers):
    """
    更新提示语
    /mgmt/sys/words/updateTrafficControlWords

    参数说明:
    - id: 主键id
    - words: 提示语
    - wordsType: 类型 0：不可发货 1：可发货但影响配送时效
    """

    url = "/mgmt/sys/words/updateTrafficControlWords"
    with client.post(url=url, json=data, headers=headers) as r:
        return r

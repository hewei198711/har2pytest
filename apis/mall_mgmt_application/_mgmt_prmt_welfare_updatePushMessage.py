import os

from util.client import client

data = {
    "id": 0,  # 主键id
    "pushMessage": False,  # 账单推送开关 true-开启 false-关闭
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_welfare_updatePushMessage(data=data, headers=headers):
    """
    修改每月账单推送消息开关
    /mgmt/prmt/welfare/updatePushMessage

    参数说明:
    - id: 主键id
    - pushMessage: 账单推送开关 true-开启 false-关闭
    """

    url = "/mgmt/prmt/welfare/updatePushMessage"
    with client.post(url=url, json=data, headers=headers) as r:
        return r

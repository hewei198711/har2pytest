import os
from urllib.parse import urlencode

from util.client import client

data = {
    "id": 0,  # id
    "pushStatus": 0,  # pushStatus
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
    "content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}


def _mgmt_store_updatePushStatus(data=data, headers=headers):
    """
    更新电子合同消息推送状态
    /mgmt/store/updatePushStatus

    参数说明:
    - id: id
    - pushStatus: pushStatus
    """

    url = "/mgmt/store/updatePushStatus"
    data = urlencode(data)  # application/x-www-form-urlencoded传参需要特殊处理

    with client.post(url=url, data=data, headers=headers) as r:
        return r

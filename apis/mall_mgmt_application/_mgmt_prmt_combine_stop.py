import os
from urllib.parse import urlencode

from util.client import client

data = {
    "id": "",  # 活动id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
    "content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}


def _mgmt_prmt_combine_stop(data=data, headers=headers):
    """
    手动停止活动
    /mgmt/prmt/combine/stop

    参数说明:
    - id: 活动id
    """

    url = "/mgmt/prmt/combine/stop"
    data = urlencode(data)  # application/x-www-form-urlencoded传参需要特殊处理

    with client.post(url=url, data=data, headers=headers) as r:
        return r

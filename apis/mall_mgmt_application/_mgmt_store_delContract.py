import os
from urllib.parse import urlencode

from util.client import client

data = {
    "id": "",  # 主键id(必填)
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
    "content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}


def _mgmt_store_delContract(data=data, headers=headers):
    """
    删除合同
    /mgmt/store/delContract

    参数说明:
    - id: 主键id(必填)
    """

    url = "/mgmt/store/delContract"
    data = urlencode(data)  # application/x-www-form-urlencoded传参需要特殊处理

    with client.post(url=url, data=data, headers=headers) as r:
        return r

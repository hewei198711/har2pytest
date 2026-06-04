import os

from util.client import client

data = {
    "id": 0,  # 主键id
    "state": False,  # 是否开启 false-否 true-是
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_sys_setInvoiceContentState(data=data, headers=headers):
    """
    配置发票采集内容开关状态
    /mgmt/sys/setInvoiceContentState

    参数说明:
    - id: 主键id
    - state: 是否开启 false-否 true-是
    """

    url = "/mgmt/sys/setInvoiceContentState"
    with client.post(url=url, json=data, headers=headers) as r:
        return r

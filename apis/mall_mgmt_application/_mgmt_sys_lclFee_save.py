import os

from util.client import client

data = {
    "amount": 0.0,  # 金额
    "feeName": "",  # 拼箱费名称
    "id": 0,  # 主键id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_sys_lclFee_save(data=data, headers=headers):
    """
    保存拼箱费模板
    /mgmt/sys/lclFee/save

    参数说明:
    - amount: 金额
    - feeName: 拼箱费名称
    - id: 主键id
    """

    url = "/mgmt/sys/lclFee/save"
    with client.post(url=url, json=data, headers=headers) as r:
        return r

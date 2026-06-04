import os

from util.client import client

data = {
    "calculation": 0,  # 计算方式1->增加；2->减少;3->不变
    "explanation": "",  # 说明
    "id": 0,  # id
    "typeName": "",  # 汇款类型名称
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_sys_updateRemittance(data=data, headers=headers):
    """
    编辑汇款类型
    /mgmt/sys/updateRemittance

    参数说明:
    - calculation: 计算方式1->增加；2->减少;3->不变
    - explanation: 说明
    - id: id
    - typeName: 汇款类型名称
    """

    url = "/mgmt/sys/updateRemittance"
    with client.post(url=url, json=data, headers=headers) as r:
        return r

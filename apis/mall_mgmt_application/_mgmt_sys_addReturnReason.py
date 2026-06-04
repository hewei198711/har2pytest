import os

from util.client import client

data = {
    "id": 0,  # id
    "parentReasonId": 0,  # 父原因id
    "returnReason": "",  # 退换货原因
    "returnType": 0,  # 退换货类型
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_sys_addReturnReason(data=data, headers=headers):
    """
    新增退换货原因
    /mgmt/sys/addReturnReason

    参数说明:
    - id: id
    - parentReasonId: 父原因id
    - returnReason: 退换货原因
    - returnType: 退换货类型
    """

    url = "/mgmt/sys/addReturnReason"
    with client.post(url=url, json=data, headers=headers) as r:
        return r

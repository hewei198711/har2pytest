import os

from util.client import client

data = {
    "amount": 0.0,  # 金额
    "effectTime": "",  # 生效时间
    "id": 0,  # 主键id
    "status": 0,  # 状态(0:立即生效,-1:待生效)
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_sys_lclFeeCeiling_update(data=data, headers=headers):
    """
    修改拼箱费上限
    /mgmt/sys/lclFeeCeiling/update

    参数说明:
    - amount: 金额
    - effectTime: 生效时间
    - id: 主键id
    - status: 状态(0:立即生效,-1:待生效)
    """

    url = "/mgmt/sys/lclFeeCeiling/update"
    with client.post(url=url, json=data, headers=headers) as r:
        return r

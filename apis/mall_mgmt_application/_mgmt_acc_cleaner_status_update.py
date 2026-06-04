import os

from util.client import client

data = {
    "id": 0,  # 清洗人id
    "remarks": "",  # 备注
    "status": 0,  # 状态 -1：已驳回 0：待审核（默认）1：审核通过
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
}


def _mgmt_acc_cleaner_status_update(data=data, headers=headers):
    """
    审核清洗人
    /mgmt/acc/cleaner/status/update

    参数说明:
    - id: 清洗人id
    - remarks: 备注
    - status: 状态 -1：已驳回 0：待审核（默认）1：审核通过
    """

    url = "/mgmt/acc/cleaner/status/update"
    with client.post(url=url, json=data, headers=headers) as r:
        return r

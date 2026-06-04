import os

from util.client import client

data = {
    "handleRemark": "",  # 备注
    "id": 0,  # 警报id
    "pageNum": 0,  # TODO: 添加参数说明
    "pageSize": 0,  # TODO: 添加参数说明
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_mortgageDeliverAlarm_removeAlarm(data=data, headers=headers):
    """
    解除预警
    /mgmt/mortgageDeliverAlarm/removeAlarm

    参数说明:
    - handleRemark: 备注
    - id: 警报id
    """

    url = "/mgmt/mortgageDeliverAlarm/removeAlarm"
    with client.post(url=url, json=data, headers=headers) as r:
        return r

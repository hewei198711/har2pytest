import os

from util.client import client

data = {
    "confStatus": 0,  # 状态，1：启用；2：禁用
    "confValue": "",  # 配置值，如时间段传2-4，其他值正常传
    "id": 0,  # 主键id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_order_riskctrl_updateWarnItemConf(data=data, headers=headers):
    """
    预警项启用/禁用，以及设置
    /mgmt/order/riskctrl/updateWarnItemConf

    参数说明:
    - confStatus: 状态，1：启用；2：禁用
    - confValue: 配置值，如时间段传2-4，其他值正常传
    - id: 主键id
    """

    url = "/mgmt/order/riskctrl/updateWarnItemConf"
    with client.post(url=url, json=data, headers=headers) as r:
        return r

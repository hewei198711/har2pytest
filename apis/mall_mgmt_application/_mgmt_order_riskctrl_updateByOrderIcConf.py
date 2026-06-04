import os

from util.client import client

data = {
    "icFlag": 0,  # 是否拦截发货，1：高风险（拦截不发货）；2：风险可控（正常发货）
    "id": 0,  # 主键id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_order_riskctrl_updateByOrderIcConf(data=data, headers=headers):
    """
    修改订单维度预警报表拦截配置
    /mgmt/order/riskctrl/updateByOrderIcConf

    参数说明:
    - icFlag: 是否拦截发货，1：高风险（拦截不发货）；2：风险可控（正常发货）
    - id: 主键id
    """

    url = "/mgmt/order/riskctrl/updateByOrderIcConf"
    with client.post(url=url, json=data, headers=headers) as r:
        return r

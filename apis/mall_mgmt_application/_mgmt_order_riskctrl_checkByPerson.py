import os

from util.client import client

data = {
    "checkRemark": "",  # 核查说明
    "handleResult": 0,  # 处理结果，1：高风险（拦截不发货）；2：风险可控（正常发货）
    "id": 0,  # 主键id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_order_riskctrl_checkByPerson(data=data, headers=headers):
    """
    人维度预警报表核查
    /mgmt/order/riskctrl/checkByPerson

    参数说明:
    - checkRemark: 核查说明
    - handleResult: 处理结果，1：高风险（拦截不发货）；2：风险可控（正常发货）
    - id: 主键id
    """

    url = "/mgmt/order/riskctrl/checkByPerson"
    with client.post(url=url, json=data, headers=headers) as r:
        return r

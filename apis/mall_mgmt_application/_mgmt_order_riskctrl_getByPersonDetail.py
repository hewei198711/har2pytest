import os

from util.client import client

data = {
    "byPersonId": 0,  # 人维度预警报表id
    "from": 0,  # TODO: 添加参数说明
    "pageNum": 0,  # 页数
    "pageSize": 0,  # 每页显示数
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_order_riskctrl_getByPersonDetail(data=data, headers=headers):
    """
    人维度预警报表查看详情
    /mgmt/order/riskctrl/getByPersonDetail

    参数说明:
    - byPersonId: 人维度预警报表id
    - pageNum: 页数
    - pageSize: 每页显示数
    """

    url = "/mgmt/order/riskctrl/getByPersonDetail"
    with client.post(url=url, json=data, headers=headers) as r:
        return r

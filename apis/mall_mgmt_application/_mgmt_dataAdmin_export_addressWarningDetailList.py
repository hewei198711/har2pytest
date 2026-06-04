import os

from util.client import client

data = {
    "detailedAddress": "",  # 收货地址
    "pageNum": 0,  # TODO: 添加参数说明
    "pageSize": 0,  # TODO: 添加参数说明
    "placeMonth": "",  # 报单月份
    "placeMonthStr": "",  # 报单月份(前端传参)
    "receiverPhone": "",  # 收货人手机号
    "ruleId": 0,  # 规则id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_dataAdmin_export_addressWarningDetailList(data=data, headers=headers):
    """
    收货地址预警详情列表导出
    /mgmt/dataAdmin/export/addressWarningDetailList

    参数说明:
    - detailedAddress: 收货地址
    - placeMonth: 报单月份
    - placeMonthStr: 报单月份(前端传参)
    - receiverPhone: 收货人手机号
    - ruleId: 规则id
    """

    url = "/mgmt/dataAdmin/export/addressWarningDetailList"
    with client.post(url=url, json=data, headers=headers) as r:
        return r

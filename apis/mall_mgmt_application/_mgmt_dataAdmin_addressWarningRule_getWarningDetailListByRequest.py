import os

from util.client import client

params = {
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


def _mgmt_dataAdmin_addressWarningRule_getWarningDetailListByRequest(params=params, headers=headers):
    """
    根据ruleId获取预警详情
    /mgmt/dataAdmin/addressWarningRule/getWarningDetailListByRequest

    参数说明:
    - detailedAddress: 收货地址
    - placeMonth: 报单月份
    - placeMonthStr: 报单月份(前端传参)
    - receiverPhone: 收货人手机号
    - ruleId: 规则id
    """

    url = "/mgmt/dataAdmin/addressWarningRule/getWarningDetailListByRequest"
    with client.get(url=url, params=params, headers=headers) as r:
        return r

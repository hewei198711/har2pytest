import os

from util.client import client

data = {
    "adjustType": 0,  # 调整类型(1押货额度,2信誉额)
    "orderAdjustTime": "",  # 调整时间排序的字段
    "pageNum": 0,  # 当前页,默认第1页
    "pageSize": 0,  # 每页显示数,默认10条
    "storeCode": "",  # 当前用户的StoreCode
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_mortgageAmount_history_mortgageAmountHistoryAdjust(data=data, headers=headers):
    """
    查询押货额度与押货信誉额调整历史:调整类型(1押货额度,2信誉额)
    /appStore/mortgageAmount/history/mortgageAmountHistoryAdjust

    参数说明:
    - adjustType: 调整类型(1押货额度,2信誉额)
    - orderAdjustTime: 调整时间排序的字段
    - pageNum: 当前页,默认第1页
    - pageSize: 每页显示数,默认10条
    - storeCode: 当前用户的StoreCode
    """

    url = "/appStore/mortgageAmount/history/mortgageAmountHistoryAdjust"
    with client.post(url=url, json=data, headers=headers) as r:
        return r

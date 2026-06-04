import os

from util.client import client

params = {
    "pageNum": 0,  # pageNum
    "pageSize": 0,  # pageSize
    "signType": 0,  # 对账单签署类型，1/1:3对账单，2/85%对账单，3/85%账款对账单，4/钱包对账单
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_queryBillJobHistoryByType(params=params, headers=headers):
    """
    通过类型查询对账单定时推送历史记录
    /mgmt/store/queryBillJobHistoryByType

    参数说明:
    - pageNum: pageNum
    - pageSize: pageSize
    - signType: 对账单签署类型，1/1:3对账单，2/85%对账单，3/85%账款对账单，4/钱包对账单
    """

    url = "/mgmt/store/queryBillJobHistoryByType"
    with client.get(url=url, params=params, headers=headers) as r:
        return r

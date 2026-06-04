import os

from util.client import client

params = {
    "promotionId": 0,  # promotionId
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_getLimitCustomerLogs(params=params, headers=headers):
    """
    查询参与活动顾客规则切换记录
    /mgmt/prmt/getLimitCustomerLogs

    参数说明:
    - promotionId: promotionId
    """

    url = "/mgmt/prmt/getLimitCustomerLogs"
    with client.get(url=url, params=params, headers=headers) as r:
        return r

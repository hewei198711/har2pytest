import os

from util.client import client

data = {
    "searchMonth": "",  # 查询月份(yyyy-MM)
    "storeCode": "",  # TODO: 添加参数说明
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_store_inventory_mortgageAmount_detailMortgageAmountChangeSum(data=data, headers=headers):
    """
    押货余额增减明细统计
    /appStore/store/inventory/mortgageAmount/detailMortgageAmountChangeSum

    参数说明:
    - searchMonth: 查询月份(yyyy-MM)
    """

    url = "/appStore/store/inventory/mortgageAmount/detailMortgageAmountChangeSum"
    with client.post(url=url, json=data, headers=headers) as r:
        return r

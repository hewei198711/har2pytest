import os

from util.client import client

params = {
    "pageNum": 0,  # 页数
    "pageSize": 0,  # 页大小
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_store_inventory_mortgageAmount_listMortgageAmountMaxRemitRecord(params=params, headers=headers):
    """
    押货最大额度调整变动明细
    /appStore/store/inventory/mortgageAmount/listMortgageAmountMaxRemitRecord

    参数说明:
    - pageNum: 页数
    - pageSize: 页大小
    """

    url = "/appStore/store/inventory/mortgageAmount/listMortgageAmountMaxRemitRecord"
    with client.get(url=url, params=params, headers=headers) as r:
        return r

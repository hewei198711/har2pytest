import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_store_inventory_mortgageAmount_getMortgageAmountByStoreCode(headers=headers):
    """
    服务中心编号获取押货额
    /appStore/store/inventory/mortgageAmount/getMortgageAmountByStoreCode
    """

    url = "/appStore/store/inventory/mortgageAmount/getMortgageAmountByStoreCode"
    with client.get(url=url, headers=headers) as r:
        return r

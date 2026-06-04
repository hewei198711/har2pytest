import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
    "content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}


def _mgmt_inventory_mortgageAmount_importMortgageAmountMaxStoreReturn(headers=headers):
    """
    服务中心退货额度批量导入
    /mgmt/inventory/mortgageAmount/importMortgageAmountMaxStoreReturn
    """

    url = "/mgmt/inventory/mortgageAmount/importMortgageAmountMaxStoreReturn"
    with client.post(url=url, headers=headers) as r:
        return r

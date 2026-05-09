import os

from util.client import client

data = {
    "money": 0.0,  # TODO: 添加参数说明
    "picPath": "",  # TODO: 添加参数说明
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_store_inventory_mortgageAmount_addMortgageAmountCreditApply(data=data, headers=headers):
    """
    申请 增加押货信誉额
    /appStore/store/inventory/mortgageAmount/addMortgageAmountCreditApply
    """

    url = "/appStore/store/inventory/mortgageAmount/addMortgageAmountCreditApply"
    with client.post(url=url, json=data, headers=headers) as r:
        return r

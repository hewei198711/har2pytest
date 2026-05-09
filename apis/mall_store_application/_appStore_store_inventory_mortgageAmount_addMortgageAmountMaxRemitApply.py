import os

from util.client import client

data = {
    "applyRemark": "",  # TODO: 添加参数说明
    "money": 0.0,  # TODO: 添加参数说明
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_store_inventory_mortgageAmount_addMortgageAmountMaxRemitApply(data=data, headers=headers):
    """
    申请 增加押货额度
    /appStore/store/inventory/mortgageAmount/addMortgageAmountMaxRemitApply
    """

    url = "/appStore/store/inventory/mortgageAmount/addMortgageAmountMaxRemitApply"
    with client.post(url=url, json=data, headers=headers) as r:
        return r

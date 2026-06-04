import os

from util.client import client

params = {
    "applyRemark": "",  # applyRemark
    "money": 0.0,  # money
    "storeCode": "",  # storeCode
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_mortgageAmount_addMortgageAmountMaxRemitApply(params=params, headers=headers):
    """
    押货额度变更申请
    /mgmt/inventory/mortgageAmount/addMortgageAmountMaxRemitApply

    参数说明:
    - applyRemark: applyRemark
    - money: money
    - storeCode: storeCode
    """

    url = "/mgmt/inventory/mortgageAmount/addMortgageAmountMaxRemitApply"
    with client.get(url=url, params=params, headers=headers) as r:
        return r

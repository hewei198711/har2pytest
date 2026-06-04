import os

from util.client import client

params = {
    "applyRemark": "",  # applyRemark
    "endTime": "",  # endTime
    "money": 0.0,  # money
    "storeCode": "",  # storeCode
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_mortgageAmount_addMortgageAmountCreditApply(params=params, headers=headers):
    """
    押货信誉额变更申请
    /mgmt/inventory/mortgageAmount/addMortgageAmountCreditApply

    参数说明:
    - applyRemark: applyRemark
    - endTime: endTime
    - money: money
    - storeCode: storeCode
    """

    url = "/mgmt/inventory/mortgageAmount/addMortgageAmountCreditApply"
    with client.get(url=url, params=params, headers=headers) as r:
        return r

import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
    "content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}


def _mgmt_inventory_mortgageAmount_importMortgageAmountMaxRemitApply(headers=headers):
    """
    服务中心押货额度批量调整导入
    /mgmt/inventory/mortgageAmount/importMortgageAmountMaxRemitApply
    """

    url = "/mgmt/inventory/mortgageAmount/importMortgageAmountMaxRemitApply"
    with client.post(url=url, headers=headers) as r:
        return r

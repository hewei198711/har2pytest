import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_mortgageAmount_exportMortgageAmountCreditTemplate(headers=headers):
    """
    服务中心信誉额批量调整模板下载
    /mgmt/inventory/mortgageAmount/exportMortgageAmountCreditTemplate
    """

    url = "/mgmt/inventory/mortgageAmount/exportMortgageAmountCreditTemplate"
    with client.get(url=url, headers=headers) as r:
        return r

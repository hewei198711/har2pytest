import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_mortgageAmount_exportMortgageAmountMaxRemitTemplate(headers=headers):
    """
    服务中心押货额批量调整模板下载
    /mgmt/inventory/mortgageAmount/exportMortgageAmountMaxRemitTemplate
    """

    url = "/mgmt/inventory/mortgageAmount/exportMortgageAmountMaxRemitTemplate"
    with client.get(url=url, headers=headers) as r:
        return r

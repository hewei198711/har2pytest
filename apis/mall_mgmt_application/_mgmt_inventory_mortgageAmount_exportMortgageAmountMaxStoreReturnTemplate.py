import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_mortgageAmount_exportMortgageAmountMaxStoreReturnTemplate(headers=headers):
    """
    服务中心退货额度批量导入模版下载
    /mgmt/inventory/mortgageAmount/exportMortgageAmountMaxStoreReturnTemplate
    """

    url = "/mgmt/inventory/mortgageAmount/exportMortgageAmountMaxStoreReturnTemplate"
    with client.get(url=url, headers=headers) as r:
        return r

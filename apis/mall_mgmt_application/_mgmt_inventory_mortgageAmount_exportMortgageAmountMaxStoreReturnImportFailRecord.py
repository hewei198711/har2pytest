import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_mortgageAmount_exportMortgageAmountMaxStoreReturnImportFailRecord(headers=headers):
    """
    导出服务中心退货额度批量导入失败的记录
    /mgmt/inventory/mortgageAmount/exportMortgageAmountMaxStoreReturnImportFailRecord
    """

    url = "/mgmt/inventory/mortgageAmount/exportMortgageAmountMaxStoreReturnImportFailRecord"
    with client.get(url=url, headers=headers) as r:
        return r

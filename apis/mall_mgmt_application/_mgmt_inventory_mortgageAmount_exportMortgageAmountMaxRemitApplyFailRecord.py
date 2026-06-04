import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_mortgageAmount_exportMortgageAmountMaxRemitApplyFailRecord(headers=headers):
    """
    服务中心押货额度批量调整导入失败记录导出
    /mgmt/inventory/mortgageAmount/exportMortgageAmountMaxRemitApplyFailRecord
    """

    url = "/mgmt/inventory/mortgageAmount/exportMortgageAmountMaxRemitApplyFailRecord"
    with client.get(url=url, headers=headers) as r:
        return r

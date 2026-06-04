import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_fin_wallet_credit_exportCreditApplyTemplate(headers=headers):
    """
    单个信用额录入及审核批量模板下载(商城后台)
    /mgmt/fin/wallet/credit/exportCreditApplyTemplate
    """

    url = "/mgmt/fin/wallet/credit/exportCreditApplyTemplate"
    with client.get(url=url, headers=headers) as r:
        return r

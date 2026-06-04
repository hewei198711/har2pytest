import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_fin_wallet_credit_stages_exportCreditStagesTemplate(headers=headers):
    """
    信用额分期模版下载(商城后台)
    /mgmt/fin/wallet/credit/stages/exportCreditStagesTemplate
    """

    url = "/mgmt/fin/wallet/credit/stages/exportCreditStagesTemplate"
    with client.get(url=url, headers=headers) as r:
        return r

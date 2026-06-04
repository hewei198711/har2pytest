import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
    "content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}


def _mgmt_fin_wallet_credit_stages_importCreditStagesData(headers=headers):
    """
    导入信用额分期管理数据
    /mgmt/fin/wallet/credit/stages/importCreditStagesData
    """

    url = "/mgmt/fin/wallet/credit/stages/importCreditStagesData"
    with client.post(url=url, headers=headers) as r:
        return r

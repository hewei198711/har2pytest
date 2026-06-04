import os

from util.client import client

params = {
    "batchNo": "",  # batchNo
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_fin_wallet_cancelControlCashierConfig(params=params, headers=headers):
    """
    取消管控列表
    /mgmt/fin/wallet/cancelControlCashierConfig

    参数说明:
    - batchNo: batchNo
    """

    url = "/mgmt/fin/wallet/cancelControlCashierConfig"
    with client.get(url=url, params=params, headers=headers) as r:
        return r

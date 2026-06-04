import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
    "content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}


def _mgmt_fin_wallet_queryFinWalletFeeRate(headers=headers):
    """
    获取重算费率配置信息列表
    /mgmt/fin/wallet/queryFinWalletFeeRate
    """

    url = "/mgmt/fin/wallet/queryFinWalletFeeRate"
    with client.post(url=url, headers=headers) as r:
        return r

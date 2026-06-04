import os

from util.client import client

data = {
    "id": 0,  # id
    "recalculateFeeRate": 0.0,  # 重算费率（结）
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_fin_wallet_updateFinWalletFeeRateDatail(data=data, headers=headers):
    """
    重算费率配置信息编辑保存
    /mgmt/fin/wallet/updateFinWalletFeeRateDatail

    参数说明:
    - id: id
    - recalculateFeeRate: 重算费率（结）
    """

    url = "/mgmt/fin/wallet/updateFinWalletFeeRateDatail"
    with client.post(url=url, json=data, headers=headers) as r:
        return r

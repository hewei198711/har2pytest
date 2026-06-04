import os
from urllib.parse import urlencode

from util.client import client

data = {
    "feeMonth": "",  # feeMonth
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
    "content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}


def _mgmt_fin_wallet_updateWalletFeeOperationInfo(data=data, headers=headers):
    """
    手续费新增处理功能
    /mgmt/fin/wallet/updateWalletFeeOperationInfo

    参数说明:
    - feeMonth: feeMonth
    """

    url = "/mgmt/fin/wallet/updateWalletFeeOperationInfo"
    data = urlencode(data)  # application/x-www-form-urlencoded传参需要特殊处理

    with client.post(url=url, data=data, headers=headers) as r:
        return r

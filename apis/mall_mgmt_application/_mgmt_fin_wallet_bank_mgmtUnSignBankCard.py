import os
from urllib.parse import urlencode

from util.client import client

data = {
    "id": 0,  # id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
    "content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}


def _mgmt_fin_wallet_bank_mgmtUnSignBankCard(data=data, headers=headers):
    """
    签约银行卡解除签约业务（商城后台）
    /mgmt/fin/wallet/bank/mgmtUnSignBankCard

    参数说明:
    - id: id
    """

    url = "/mgmt/fin/wallet/bank/mgmtUnSignBankCard"
    data = urlencode(data)  # application/x-www-form-urlencoded传参需要特殊处理

    with client.post(url=url, data=data, headers=headers) as r:
        return r

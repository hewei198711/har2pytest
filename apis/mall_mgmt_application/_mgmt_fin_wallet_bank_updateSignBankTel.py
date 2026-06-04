import os
from urllib.parse import urlencode

from util.client import client

data = {
    "id": 0,  # id
    "tel": "",  # tel
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
    "content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}


def _mgmt_fin_wallet_bank_updateSignBankTel(data=data, headers=headers):
    """
    签约银行卡信息更新手机号(商城后台)
    /mgmt/fin/wallet/bank/updateSignBankTel

    参数说明:
    - id: id
    - tel: tel
    """

    url = "/mgmt/fin/wallet/bank/updateSignBankTel"
    data = urlencode(data)  # application/x-www-form-urlencoded传参需要特殊处理

    with client.post(url=url, data=data, headers=headers) as r:
        return r

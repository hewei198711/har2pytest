import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
    "content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}


def _mgmt_pay_verifyAcct_queryAllCcbSignBankAccount(headers=headers):
    """
    查询新建行B端签约卡
    /mgmt/pay/verifyAcct/queryAllCcbSignBankAccount
    """

    url = "/mgmt/pay/verifyAcct/queryAllCcbSignBankAccount"
    with client.post(url=url, headers=headers) as r:
        return r

import os

from util.client import client

params = {
    "isSigned": "",  # 是否已签约，1/是，2/否
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_store_getSignBankAccountList(params=params, headers=headers):
    """
    获取签约银行列表
    /appStore/store/getSignBankAccountList

    参数说明:
    - isSigned: 是否已签约，1/是，2/否
    """

    url = "/appStore/store/getSignBankAccountList"
    with client.get(url=url, params=params, headers=headers) as r:
        return r

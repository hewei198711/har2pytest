import os

from util.client import client

params = {
    "cardNo": "",  # cardNo
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
}


def _appStore_crm_bmemberbank_getMerberBankListByCardNo(params=params, headers=headers):
    """
    会员发放银行卡查询-app端查列表
    /appStore/crm/bmemberbank/getMerberBankListByCardNo

    参数说明:
    - cardNo: cardNo
    """

    url = "/appStore/crm/bmemberbank/getMerberBankListByCardNo"
    with client.get(url=url, params=params, headers=headers) as r:
        return r

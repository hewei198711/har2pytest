import os

from util.client import client

params = {
    "memberId": 0,  # memberId
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
}


def _appStore_crm_bmemberbank_deletebyMemberId(params=params, headers=headers):
    """
    根据会员id删除银行卡/解绑
    /appStore/crm/bmemberbank/deletebyMemberId

    参数说明:
    - memberId: memberId
    """

    url = "/appStore/crm/bmemberbank/deletebyMemberId"
    with client.get(url=url, params=params, headers=headers) as r:
        return r

import os

from util.client import client

params = {
    "memberCardNo": "",  # 会员卡号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_queryRegisterStatusByCardNo(params=params, headers=headers):
    """
    通过会员卡号查询商城会员注册状态
    /mgmt/store/queryRegisterStatusByCardNo

    参数说明:
    - memberCardNo: 会员卡号
    """

    url = "/mgmt/store/queryRegisterStatusByCardNo"
    with client.get(url=url, params=params, headers=headers) as r:
        return r

import os

from util.client import client

data = {
    "cardNo": "",  # 会员卡号
    "mobile": "",  # 会员手机号码
    "storeCode": "",  # 最大购货店
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_store_common_updateMemberMobile(data=data, headers=headers):
    """
    修改会员手机号码
    /appStore/store/common/updateMemberMobile

    参数说明:
    - cardNo: 会员卡号
    - mobile: 会员手机号码
    - storeCode: 最大购货店
    """

    url = "/appStore/store/common/updateMemberMobile"
    with client.post(url=url, json=data, headers=headers) as r:
        return r

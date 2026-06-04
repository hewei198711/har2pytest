import os

from util.client import client

params = {
    "isEdit": False,  # isEdit
    "loginGiftId": 0,  # loginGiftId
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_loginGift_getLoginGift(params=params, headers=headers):
    """
    查询登录有礼活动信息
    /mgmt/prmt/loginGift/getLoginGift

    参数说明:
    - isEdit: isEdit
    - loginGiftId: loginGiftId
    """

    url = "/mgmt/prmt/loginGift/getLoginGift"
    with client.get(url=url, params=params, headers=headers) as r:
        return r

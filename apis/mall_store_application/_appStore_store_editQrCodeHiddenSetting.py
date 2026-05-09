import os

from util.client import client

data = {
    "orderIsHidden": False,  # 订单详情活码是否隐藏,false-否，true-是
    "orderQrShowType": 0,  # 订单详情展示类型 1管理员活码 2配偶活码
    "storeIsHidden": False,  # 门店导航活码是否隐藏,false-否，true-是
    "storeQrShowType": 0,  # 门店导航展示类型 1管理员活码 2配偶活码
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_store_editQrCodeHiddenSetting(data=data, headers=headers):
    """
    编辑活码是否隐藏
    /appStore/store/editQrCodeHiddenSetting

    参数说明:
    - orderIsHidden: 订单详情活码是否隐藏,false-否，true-是
    - orderQrShowType: 订单详情展示类型 1管理员活码 2配偶活码
    - storeIsHidden: 门店导航活码是否隐藏,false-否，true-是
    - storeQrShowType: 门店导航展示类型 1管理员活码 2配偶活码
    """

    url = "/appStore/store/editQrCodeHiddenSetting"
    with client.post(url=url, json=data, headers=headers) as r:
        return r

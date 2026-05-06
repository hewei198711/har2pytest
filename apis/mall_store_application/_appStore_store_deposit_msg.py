from util.client import client

params = {
    "storeCode": "914008",  # 店铺编号
}

headers = {"channel": "pc", "client": "store", "authorization": "请输入认证令牌"}


def _appStore_store_deposit_msg(params=params, headers=headers):
    """
    获取服务中心可用押货保证金余额
    /appStore/store/deposit/msg

    参数说明:
    - month: 月份yyyy-MM
    - storeCode: 店铺编号
    """

    url = "/appStore/store/deposit/msg"
    with client.get(url=url, params=params, headers=headers) as r:
        return r

import os

from util.client import client

params = {
    "cardNo": "",  # 云商会员卡号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_getYsStoreInfo(params=params, headers=headers):
    """
    获取云商服务中心信息（主要提供给《结算后销售调整》使用）
    /mgmt/store/getYsStoreInfo

    参数说明:
    - cardNo: 云商会员卡号
    """

    url = "/mgmt/store/getYsStoreInfo"
    with client.get(url=url, params=params, headers=headers) as r:
        return r

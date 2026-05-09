import os

from util.client import client

params = {
    "type": 0,  # 类型: 3退货 4换货
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
}


def _appStore_common_getReason(params=params, headers=headers):
    """
    获取各种退换货原因
    /appStore/common/getReason

    参数说明:
    - type: 类型: 3退货 4换货
    """

    url = "/appStore/common/getReason"
    with client.get(url=url, params=params, headers=headers) as r:
        return r

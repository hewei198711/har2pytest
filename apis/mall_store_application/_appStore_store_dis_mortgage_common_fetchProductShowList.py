import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_store_dis_mortgage_common_fetchProductShowList(headers=headers):
    """
    获取商品前端分类列表
    /appStore/store/dis/mortgage/common/fetchProductShowList
    """

    url = "/appStore/store/dis/mortgage/common/fetchProductShowList"
    with client.get(url=url, headers=headers) as r:
        return r

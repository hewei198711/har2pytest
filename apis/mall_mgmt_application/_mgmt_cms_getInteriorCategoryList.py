import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_getInteriorCategoryList(headers=headers):
    """
    获取商品中心内部分类
    /mgmt/cms/getInteriorCategoryList
    """

    url = "/mgmt/cms/getInteriorCategoryList"
    with client.get(url=url, headers=headers) as r:
        return r

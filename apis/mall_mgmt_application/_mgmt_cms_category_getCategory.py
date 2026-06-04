import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
}


def _mgmt_cms_category_getCategory(headers=headers):
    """
    获取商品分类
    /mgmt/cms/category/getCategory
    """

    url = "/mgmt/cms/category/getCategory"
    with client.get(url=url, headers=headers) as r:
        return r

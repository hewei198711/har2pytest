import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_product_item_getCusItemTemplate(headers=headers):
    """
    获取定制产品批量导入模板
    /mgmt/product/item/getCusItemTemplate
    """

    url = "/mgmt/product/item/getCusItemTemplate"
    with client.get(url=url, headers=headers) as r:
        return r

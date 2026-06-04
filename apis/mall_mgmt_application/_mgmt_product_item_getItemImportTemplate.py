import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_product_item_getItemImportTemplate(headers=headers):
    """
    获取产品批量导入模板
    /mgmt/product/item/getItemImportTemplate
    """

    url = "/mgmt/product/item/getItemImportTemplate"
    with client.get(url=url, headers=headers) as r:
        return r

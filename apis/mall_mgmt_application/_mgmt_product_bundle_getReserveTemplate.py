import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_product_bundle_getReserveTemplate(headers=headers):
    """
    获取保留套装批量导入模板
    /mgmt/product/bundle/getReserveTemplate
    """

    url = "/mgmt/product/bundle/getReserveTemplate"
    with client.get(url=url, headers=headers) as r:
        return r

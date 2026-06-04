import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_product_quota_getDistImportTemplate(headers=headers):
    """
    获取服务中心销售分配量导入模板
    /mgmt/product/quota/getDistImportTemplate
    """

    url = "/mgmt/product/quota/getDistImportTemplate"
    with client.get(url=url, headers=headers) as r:
        return r

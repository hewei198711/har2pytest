import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_product_quota_exportProductDistFailRecord(headers=headers):
    """
    销售分配量批量导入失败记录导出
    /mgmt/product/quota/exportProductDistFailRecord
    """

    url = "/mgmt/product/quota/exportProductDistFailRecord"
    with client.get(url=url, headers=headers) as r:
        return r

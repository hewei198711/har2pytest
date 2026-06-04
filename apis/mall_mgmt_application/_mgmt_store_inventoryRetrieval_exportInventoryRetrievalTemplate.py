import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_inventoryRetrieval_exportInventoryRetrievalTemplate(headers=headers):
    """
    服务中心库存检索批量导入模板下载
    /mgmt/store/inventoryRetrieval/exportInventoryRetrievalTemplate
    """

    url = "/mgmt/store/inventoryRetrieval/exportInventoryRetrievalTemplate"
    with client.get(url=url, headers=headers) as r:
        return r

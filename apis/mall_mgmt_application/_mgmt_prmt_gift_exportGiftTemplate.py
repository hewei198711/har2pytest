import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_gift_exportGiftTemplate(headers=headers):
    """
    导入赠品模板下载
    /mgmt/prmt/gift/exportGiftTemplate
    """

    url = "/mgmt/prmt/gift/exportGiftTemplate"
    with client.get(url=url, headers=headers) as r:
        return r

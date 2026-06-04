import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_exportBatchAdjustLevelTemplate(headers=headers):
    """
    服务中心批量调整等级  模板下载
    /mgmt/store/exportBatchAdjustLevelTemplate
    """

    url = "/mgmt/store/exportBatchAdjustLevelTemplate"
    with client.get(url=url, headers=headers) as r:
        return r

import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_exportBatchAdjustLevelFailRecord(headers=headers):
    """
    服务中心批量调整等级失败记录导出
    /mgmt/store/exportBatchAdjustLevelFailRecord
    """

    url = "/mgmt/store/exportBatchAdjustLevelFailRecord"
    with client.get(url=url, headers=headers) as r:
        return r

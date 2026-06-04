import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_awardRecord_exportFailRecord(headers=headers):
    """
    获奖记录导入失败记录导出
    /mgmt/store/awardRecord/exportFailRecord
    """

    url = "/mgmt/store/awardRecord/exportFailRecord"
    with client.get(url=url, headers=headers) as r:
        return r

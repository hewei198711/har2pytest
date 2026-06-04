import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_awardRecord_templateDownload(headers=headers):
    """
    服务中心获奖记录导入模板下载
    /mgmt/store/awardRecord/templateDownload
    """

    url = "/mgmt/store/awardRecord/templateDownload"
    with client.get(url=url, headers=headers) as r:
        return r

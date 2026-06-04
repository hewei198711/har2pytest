import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_annualReview_exportFailRecord(headers=headers):
    """
    年审控制批量导入失败记录导出
    /mgmt/store/annualReview/exportFailRecord
    """

    url = "/mgmt/store/annualReview/exportFailRecord"
    with client.get(url=url, headers=headers) as r:
        return r

import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
    "content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}


def _mgmt_store_annualReview_importBatch(headers=headers):
    """
    年审控制批量导入
    /mgmt/store/annualReview/importBatch
    """

    url = "/mgmt/store/annualReview/importBatch"
    with client.post(url=url, headers=headers) as r:
        return r

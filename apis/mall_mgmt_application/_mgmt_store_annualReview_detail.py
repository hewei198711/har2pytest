import os

from util.client import client

params = {
    "applyId": 0,  # applyId
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_annualReview_detail(params=params, headers=headers):
    """
    年审申请详情
    /mgmt/store/annualReview/detail

    参数说明:
    - applyId: applyId
    """

    url = "/mgmt/store/annualReview/detail"
    with client.get(url=url, params=params, headers=headers) as r:
        return r

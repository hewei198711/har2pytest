import os

from util.client import client

params = {
    "id": 0,  # id
    "verifyRemark": "",  # verifyRemark
    "verifyStatus": 0,  # verifyStatus
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_annualReview_verify(params=params, headers=headers):
    """
    审批
    /mgmt/store/annualReview/verify

    参数说明:
    - id: id
    - verifyRemark: verifyRemark
    - verifyStatus: verifyStatus
    """

    url = "/mgmt/store/annualReview/verify"
    with client.get(url=url, params=params, headers=headers) as r:
        return r

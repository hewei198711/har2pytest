import os

from util.client import client

data = {
    "id": 0,  # id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_couponTransfer_revokeCoupon(data=data, headers=headers):
    """
    撤销
    /mgmt/prmt/couponTransfer/revokeCoupon

    参数说明:
    - id: id
    """

    url = "/mgmt/prmt/couponTransfer/revokeCoupon"
    with client.post(url=url, json=data, headers=headers) as r:
        return r

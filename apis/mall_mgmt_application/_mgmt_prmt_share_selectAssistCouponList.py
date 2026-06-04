import os

from util.client import client

params = {
    "id": 0,  # id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_share_selectAssistCouponList(params=params, headers=headers):
    """
    查看助力券
    /mgmt/prmt/share/selectAssistCouponList

    参数说明:
    - id: id
    """

    url = "/mgmt/prmt/share/selectAssistCouponList"
    with client.get(url=url, params=params, headers=headers) as r:
        return r

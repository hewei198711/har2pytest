import os

from util.client import client

data = {
    "id": 0,  # id
    "remarks": "",  # 说明
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_coupon_editRemarks(data=data, headers=headers):
    """
    编辑优惠券使用说明
    /mgmt/prmt/coupon/editRemarks

    参数说明:
    - id: id
    - remarks: 说明
    """

    url = "/mgmt/prmt/coupon/editRemarks"
    with client.post(url=url, json=data, headers=headers) as r:
        return r

import os

from util.client import client

data = {
    "id": 0,  # id
    "remarks": "",  # 备注
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_shelvesCoupon_offShelves(data=data, headers=headers):
    """
    下架优惠券（停止）
    /mgmt/prmt/shelvesCoupon/offShelves

    参数说明:
    - id: id
    - remarks: 备注
    """

    url = "/mgmt/prmt/shelvesCoupon/offShelves"
    with client.post(url=url, json=data, headers=headers) as r:
        return r

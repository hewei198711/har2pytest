import os

from util.client import client

data = {
    "couponId": 0,  # 优惠券id
    "enclosureVos": [{"fileName": "", "urls": ""}],  # 附件集合
    "examine": 0,  # 审核是否通过3通过4不通过
    "remarks": "",  # 备注
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_coupon_examine(data=data, headers=headers):
    """
    优惠券审核
    /mgmt/prmt/coupon/examine

    参数说明:
    - couponId: 优惠券id
    - enclosureVos: 附件集合
    - enclosureVos.fileName: 附件名称
    - enclosureVos.urls: 附件地址
    - examine: 审核是否通过3通过4不通过
    - remarks: 备注
    """

    url = "/mgmt/prmt/coupon/examine"
    with client.post(url=url, json=data, headers=headers) as r:
        return r

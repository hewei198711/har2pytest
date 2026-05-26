import os

from util.client import client

data = {
    "promotionId": None,  # TODO: 添加参数说明
    "examine": 3,  # 审核是否通过3通过4不通过
    "remarks": "111",  # 备注
    "enclosureVos": [],  # 附件集合
    "couponId": "1270722876147920065",  # 优惠券id
}

headers = {
    "channel": "pc",
    "client": "op",
    "content-type": "application/json;charset=UTF-8",
    "authorization": f"bearer {os.environ['access_token']}",
}


def _mgmt_prmt_coupon_examine(data=data, headers=headers):
    """
    优惠券审核
    /mgmt/prmt/coupon/examine

    参数说明:
    - couponId: 优惠券id
    - enclosureVos: 附件集合
    - examine: 审核是否通过3通过4不通过
    - remarks: 备注
    """

    url = "/mgmt/prmt/coupon/examine"
    with client.post(url=url, json=data, headers=headers) as r:
        return r

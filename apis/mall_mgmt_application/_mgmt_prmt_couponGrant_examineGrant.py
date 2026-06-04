import os

from util.client import client

data = {
    "enclosureVos": [{"fileName": "", "urls": ""}],  # 附件集合
    "examine": 0,  # 审核是否通过3通过4不通过
    "grantId": 0,  # 优惠券派发id
    "remark": "",  # 备注
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_couponGrant_examineGrant(data=data, headers=headers):
    """
    优惠券派发审核
    /mgmt/prmt/couponGrant/examineGrant

    参数说明:
    - enclosureVos: 附件集合
    - enclosureVos.fileName: 附件名称
    - enclosureVos.urls: 附件地址
    - examine: 审核是否通过3通过4不通过
    - grantId: 优惠券派发id
    - remark: 备注
    """

    url = "/mgmt/prmt/couponGrant/examineGrant"
    with client.post(url=url, json=data, headers=headers) as r:
        return r

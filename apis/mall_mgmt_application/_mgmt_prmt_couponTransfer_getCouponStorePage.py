import os

from util.client import client

params = {
    "code": "",  # 门店编号
    "grantId": 0,  # 派发id
    "leaderNo": "",  # 负责人卡号
    "pageNum": 0,  # 当前页
    "pageSize": 0,  # 每页条数
    "shopkeeperNo": "",  # 分店管理员卡号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_couponTransfer_getCouponStorePage(params=params, headers=headers):
    """
    转赠优惠券门店分页
    /mgmt/prmt/couponTransfer/getCouponStorePage

    参数说明:
    - code: 门店编号
    - grantId: 派发id
    - leaderNo: 负责人卡号
    - pageNum: 当前页
    - pageSize: 每页条数
    - shopkeeperNo: 分店管理员卡号
    """

    url = "/mgmt/prmt/couponTransfer/getCouponStorePage"
    with client.get(url=url, params=params, headers=headers) as r:
        return r

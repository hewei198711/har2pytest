import os

from util.client import client

params = {
    "couponState": 0,  # 兑换状态: null- 表示查询全部, 0-未兑换, 1-已兑换
    "id": 0,  # id
    "pageNum": 0,  # 当前页
    "pageSize": 0,  # 每页数量
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_giftPromotion_giftCodePage(params=params, headers=headers):
    """
    赠品码列表分页查询
    /mgmt/prmt/giftPromotion/giftCodePage

    参数说明:
    - couponState: 兑换状态: null- 表示查询全部, 0-未兑换, 1-已兑换
    - id: id
    - pageNum: 当前页
    - pageSize: 每页数量
    """

    url = "/mgmt/prmt/giftPromotion/giftCodePage"
    with client.get(url=url, params=params, headers=headers) as r:
        return r

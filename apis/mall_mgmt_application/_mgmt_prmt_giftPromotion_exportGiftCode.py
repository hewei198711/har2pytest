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


def _mgmt_prmt_giftPromotion_exportGiftCode(params=params, headers=headers):
    """
    导出赠品兑换码
    /mgmt/prmt/giftPromotion/exportGiftCode

    参数说明:
    - couponState: 兑换状态: null- 表示查询全部, 0-未兑换, 1-已兑换
    - id: id
    - pageNum: 当前页
    - pageSize: 每页数量
    """

    url = "/mgmt/prmt/giftPromotion/exportGiftCode"
    with client.get(url=url, params=params, headers=headers) as r:
        return r

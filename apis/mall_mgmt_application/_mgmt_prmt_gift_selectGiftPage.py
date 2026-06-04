import os

from util.client import client

params = {
    "cardNo": "",  # 会员卡号
    "getTimeMax": "",  # 获赠时间止yyyy-MM
    "getTimeMin": "",  # 获赠时间起yyyy-MM
    "giftCode": "",  # 赠品编码
    "giftName": "",  # 赠品名称
    "id": 0,  # 赠品派发任务id
    "ids": [],  # id集合
    "pageNum": 0,  # 当前页
    "pageSize": 0,  # 每页条数
    "storeCode": "",  # 服务中心编号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_gift_selectGiftPage(params=params, headers=headers):
    """
    分页查询赠品
    /mgmt/prmt/gift/selectGiftPage

    参数说明:
    - cardNo: 会员卡号
    - getTimeMax: 获赠时间止yyyy-MM
    - getTimeMin: 获赠时间起yyyy-MM
    - giftCode: 赠品编码
    - giftName: 赠品名称
    - id: 赠品派发任务id
    - ids: id集合
    - pageNum: 当前页
    - pageSize: 每页条数
    - storeCode: 服务中心编号
    """

    url = "/mgmt/prmt/gift/selectGiftPage"
    with client.get(url=url, params=params, headers=headers) as r:
        return r

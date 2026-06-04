import os

from util.client import client

params = {
    "cardNo": "",  # 会员卡号
    "couponCode": "",  # 兑换码
    "couponState": 0,  # 赠品状态:1-未使用, 2-已使用, 4-已失效
    "getType": 0,  # 获得方式:0-用户领取,1-抽奖活动
    "id": 0,  # id
    "mobile": "",  # 手机号码
    "pageNum": 0,  # 当前页
    "pageSize": 0,  # 每页数量
    "platform": 0,  # 领取平台:1-APP, 2-PC, 4-小程序
    "realName": "",  # 真实姓名
    "usedPlatform": 0,  # 使用平台:1-APP, 2-PC, 4-小程序
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_giftPromotion_giftInfoPageData(params=params, headers=headers):
    """
    赠品领用详情列表分页查询 -- 统计数据
    /mgmt/prmt/giftPromotion/giftInfoPageData

    参数说明:
    - cardNo: 会员卡号
    - couponCode: 兑换码
    - couponState: 赠品状态:1-未使用, 2-已使用, 4-已失效
    - getType: 获得方式:0-用户领取,1-抽奖活动
    - id: id
    - mobile: 手机号码
    - pageNum: 当前页
    - pageSize: 每页数量
    - platform: 领取平台:1-APP, 2-PC, 4-小程序
    - realName: 真实姓名
    - usedPlatform: 使用平台:1-APP, 2-PC, 4-小程序
    """

    url = "/mgmt/prmt/giftPromotion/giftInfoPageData"
    with client.get(url=url, params=params, headers=headers) as r:
        return r

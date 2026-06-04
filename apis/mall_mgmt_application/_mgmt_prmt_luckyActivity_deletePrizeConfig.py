import os

from util.client import client

data = {
    "activityId": 0,  # 活动id
    "alreadyHandNumber": 0,  # 已派发数量
    "blindBoxRemark": "",  # 盲盒模式奖品文案
    "couponId": 0,  # 优惠券id
    "limitHandNumber": 0,  # 奖品限制派发数量
    "mobileRegion": "",  # 移动端刮刮乐区域配置
    "mobileResultPicture": "",  # 移动端抽奖结果图片地址(刮刮乐)
    "onceBeanAmount": 0,  # 每份奖品金豆数量
    "pcRegion": "",  # PC端刮刮乐区域配置
    "pcResultPicture": "",  # PC抽奖结果图片地址(刮刮乐)
    "prizeHandType": 0,  # 奖品派发数量类型(1:不限量；2;限制派发)
    "prizeId": 0,  # 奖品id
    "prizeName": "",  # 奖品名称
    "prizePicture": "",  # 奖品图片
    "prizeType": 0,  # 奖品类型：1-优惠券，2-赠品兑换码活动 3-金豆
    "sourceId": 0,  # 奖品来源id：兑换活动id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_luckyActivity_deletePrizeConfig(data=data, headers=headers):
    """
    删除活动奖品
    /mgmt/prmt/luckyActivity/deletePrizeConfig

    参数说明:
    - activityId: 活动id
    - alreadyHandNumber: 已派发数量
    - blindBoxRemark: 盲盒模式奖品文案
    - couponId: 优惠券id
    - limitHandNumber: 奖品限制派发数量
    - mobileRegion: 移动端刮刮乐区域配置
    - mobileResultPicture: 移动端抽奖结果图片地址(刮刮乐)
    - onceBeanAmount: 每份奖品金豆数量
    - pcRegion: PC端刮刮乐区域配置
    - pcResultPicture: PC抽奖结果图片地址(刮刮乐)
    - prizeHandType: 奖品派发数量类型(1:不限量；2;限制派发)
    - prizeId: 奖品id
    - prizeName: 奖品名称
    - prizePicture: 奖品图片
    - prizeType: 奖品类型：1-优惠券，2-赠品兑换码活动 3-金豆
    - sourceId: 奖品来源id：兑换活动id
    """

    url = "/mgmt/prmt/luckyActivity/deletePrizeConfig"
    with client.post(url=url, json=data, headers=headers) as r:
        return r

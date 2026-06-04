import os

from util.client import client

data = {
    "activityId": 0,  # 活动id
    "blindBoxRemark": "",  # 盲盒模式不中奖奖品文案
    "couponId": 0,  # 优惠券id
    "isGetCoupon": 0,  # 是否获券(0:否;1:是)
    "limitHandNumber": 0,  # 奖品限制派发数量
    "mobileRegion": "",  # 移动端刮刮乐区域配置
    "mobileResultPicture": "",  # 移动端抽奖结果图片地址(刮刮乐)
    "npId": 0,  # 不中奖配置id
    "pcRegion": "",  # PC端刮刮乐区域配置
    "pcResultPicture": "",  # PC抽奖结果图片地址(刮刮乐)
    "prizeHandType": 0,  # 奖品派发数量类型(1:不限量；2;限制派发)
    "prizeName": "",  # 奖品名称
    "prizePicture": "",  # 奖品图片
    "tips": "",  # 提示语
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_luckyActivity_editNotPrizeConfigCoupon(data=data, headers=headers):
    """
    删除不中奖配置关联优惠券
    /mgmt/prmt/luckyActivity/editNotPrizeConfigCoupon

    参数说明:
    - activityId: 活动id
    - blindBoxRemark: 盲盒模式不中奖奖品文案
    - couponId: 优惠券id
    - isGetCoupon: 是否获券(0:否;1:是)
    - limitHandNumber: 奖品限制派发数量
    - mobileRegion: 移动端刮刮乐区域配置
    - mobileResultPicture: 移动端抽奖结果图片地址(刮刮乐)
    - npId: 不中奖配置id
    - pcRegion: PC端刮刮乐区域配置
    - pcResultPicture: PC抽奖结果图片地址(刮刮乐)
    - prizeHandType: 奖品派发数量类型(1:不限量；2;限制派发)
    - prizeName: 奖品名称
    - prizePicture: 奖品图片
    - tips: 提示语
    """

    url = "/mgmt/prmt/luckyActivity/editNotPrizeConfigCoupon"
    with client.post(url=url, json=data, headers=headers) as r:
        return r

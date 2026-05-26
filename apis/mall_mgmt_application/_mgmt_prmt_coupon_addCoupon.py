import os

from util.client import client

data = {
    "orderWayList": [1, 2],  # 下单限制1自购2代购
    "platforms": [1, 2, 4],  # 限制平台1app2pc4小程序
    "limitStore": 0,  # 是否限制门店0否1是2代购限门店
    "categoryIds": [],  # 分类id集合
    "couponCount": 1000,  # 优惠券总量-1不限量
    "limitCount": None,  # 可获得数量（null不限）
    "couponName": "威威抽奖品",  # 名称
    "couponNumber": "ww051901",  # 编号
    "couponState": 1,  # 状态1待审核2待生效3生效中4已失效5已禁用6已驳回7草稿
    "couponType": 1,  # 优惠券类型:1-立减券,2-满减券,3-叠加满减券,4-堆叠满减券,5-产品兑换券
    "endTime": None,  # 失效时间（不填表示一直有效）
    "endType": 4,  # 失效方式:1-定时失效 2-不限制 3-N个自然日 4-N个自然月
    "faceValue": 10,  # 面值
    "grantCount": 0,  # 已发放数量
    "isGenerateCode": 0,  # 是否生成优惠码0不生成1生成
    "isScanCode": 0,  # 是否生成太阳码 0: 不生成  1: 生成
    "isStacked": 0,  # 是否可叠加0不可叠加1可叠加
    "transferable": False,  # 是否支持顾客转赠 true:支持  false:不支持
    "minAmount": None,  # 使用条件
    "promotionIds": [],  # 活动id集合
    "remarks": "111111111111",  # 说明
    "serialNos": [],  # 可用商品集合
    "disableSerialNos": [],  # 不可用商品集合
    "startTime": None,  # 生效时间
    "startTimeType": 0,  # TODO: 添加参数说明
    "useRange": 1,  # 使用范围:1-所有产品,2-指定产品,3-指定不适用产品,4-指定产品分类,5-指定活动6-指定签约购3.0活动,7-签约购4.0活动
    "usedCount": 0,  # 已核销数量
    "stackTimes": "",  # 叠加上限(null不限制)
    "activeDay": 1,  # 有效天数 或 有效自然月数
    "activeMonth": 1,  # TODO: 添加参数说明
    "performance": True,  # 是否计算业绩：true:是  false:否
    "productConditions": 1,  # TODO: 添加参数说明
    "productMinAmount": 1,  # TODO: 添加参数说明
    "minAmountType": 1,  # 使用条件限制类型,与属性minAmount搭配使用：1-金额, 2-PV
    "transferableLimitCustomer": 1,  # C端转赠对象限制：1-所有顾客,2-自定义顾客群
    "memberCustom": None,  # 自定义顾客群
    "startType": 2,  # 开始生效方式1定时生效2派发后生效
    "receiveRemarks": "112222222222222222",  # 领券说明(目前只在领取中心展示)
}

headers = {
    "channel": "pc",
    "client": "op",
    "content-type": "application/json;charset=UTF-8",
    "authorization": f"bearer {os.environ['access_token']}",
}


def _mgmt_prmt_coupon_addCoupon(data=data, headers=headers):
    """
    保存新建的优惠券
    /mgmt/prmt/coupon/addCoupon

    参数说明:
    - activeDay: 有效天数 或 有效自然月数
    - categoryIds: 分类id集合
    - couponCount: 优惠券总量-1不限量
    - couponName: 名称
    - couponNumber: 编号
    - couponState: 状态1待审核2待生效3生效中4已失效5已禁用6已驳回7草稿
    - couponType: 优惠券类型:1-立减券,2-满减券,3-叠加满减券,4-堆叠满减券,5-产品兑换券
    - disableSerialNos: 不可用商品集合
    - endTime: 失效时间（不填表示一直有效）
    - endType: 失效方式:1-定时失效 2-不限制 3-N个自然日 4-N个自然月
    - faceValue: 面值
    - grantCount: 已发放数量
    - invalidCount: 已作废数量
    - isGenerateCode: 是否生成优惠码0不生成1生成
    - isScanCode: 是否生成太阳码 0: 不生成  1: 生成
    - isStacked: 是否可叠加0不可叠加1可叠加
    - limitCount: 可获得数量（null不限）
    - limitStore: 是否限制门店0否1是2代购限门店
    - memberCustom: 自定义顾客群
    - minAmount: 使用条件
    - minAmountType: 使用条件限制类型,与属性minAmount搭配使用：1-金额, 2-PV
    - occupyCount: 占用中数量
    - orderWayList: 下单限制1自购2代购
    - performance: 是否计算业绩：true:是  false:否
    - platforms: 限制平台1app2pc4小程序
    - promotionIds: 活动id集合
    - receiveRemarks: 领券说明(目前只在领取中心展示)
    - remarks: 说明
    - serialNos: 可用商品集合
    - stackTimes: 叠加上限(null不限制)
    - startTime: 生效时间
    - startType: 开始生效方式1定时生效2派发后生效
    - transferable: 是否支持顾客转赠 true:支持  false:不支持
    - transferableLimitCustomer: C端转赠对象限制：1-所有顾客,2-自定义顾客群
    - useRange: 使用范围:1-所有产品,2-指定产品,3-指定不适用产品,4-指定产品分类,5-指定活动6-指定签约购3.0活动,7-签约购4.0活动
    - usedCount: 已核销数量
    """

    url = "/mgmt/prmt/coupon/addCoupon"
    with client.post(url=url, json=data, headers=headers) as r:
        return r

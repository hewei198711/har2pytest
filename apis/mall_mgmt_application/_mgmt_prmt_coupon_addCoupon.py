import os

from util.client import client

data = {
    "activeDay": 0,  # 有效天数 或 有效自然月数
    "categoryIds": [],  # 分类id集合
    "couponCount": 0,  # 优惠券总量-1不限量
    "couponName": "",  # 名称
    "couponNumber": "",  # 编号
    "couponState": 0,  # 状态1待审核2待生效3生效中4已失效5已禁用6已驳回7草稿
    "couponType": 0,  # 优惠券类型:1-立减券,2-满减券,3-叠加满减券,4-堆叠满减券,5-产品兑换券
    "disableSerialNos": [],  # 不可用商品集合
    "endTime": "",  # 失效时间（不填表示一直有效）
    "endType": 0,  # 失效方式:1-定时失效 2-不限制 3-N个自然日 4-N个自然月
    "faceValue": 0.0,  # 面值
    "grantCount": 0,  # 已发放数量
    "id": 0,  # TODO: 添加参数说明
    "invalidCount": 0,  # 已作废数量
    "isGenerateCode": 0,  # 是否生成优惠码0不生成1生成
    "isScanCode": 0,  # 是否生成太阳码 0: 不生成  1: 生成
    "isStacked": 0,  # 是否可叠加0不可叠加1可叠加
    "limitCount": 0,  # 可获得数量（null不限）
    "limitStore": 0,  # 是否限制门店0否1是2代购限门店
    "memberCustom": {
        "cardEndDate": "",
        "cardStartDate": "",
        "cardStatuses": [],
        "hyqEndDate": "",
        "hyqStartDate": "",
        "limitCardAfter": 0,
        "limitCardBefore": 0,
        "limitCardDate": 0,
        "limitHyqAccount": 0,
        "limitHyqDate": 0,
        "limitLoginDate": 0,
        "limitMemberLevel": False,
        "limitOrderDate": 0,
        "limitPurchaseDate": 0,
        "limitRegDate": 0,
        "limitUpgradeDate": 0,
        "limitWx": 0,
        "limitWxDate": 0,
        "loginEndDate": "",
        "loginPlatforms": [],
        "loginStartDate": "",
        "memberLevels": [],
        "memberTypes": [],
        "orderEndDate": "",
        "orderStartDate": "",
        "provinceCodes": [],
        "regEndDate": "",
        "regStartDate": "",
        "upgradeEndDate": "",
        "upgradeStartDate": "",
        "wxEndDate": "",
        "wxStartDate": "",
    },  # 自定义顾客群
    "minAmount": 0.0,  # 使用条件
    "minAmountType": 0,  # 使用条件限制类型,与属性minAmount搭配使用：1-金额, 2-PV
    "occupyCount": 0,  # 占用中数量
    "orderWayList": [],  # 下单限制1自购2代购
    "performance": False,  # 是否计算业绩：true:是  false:否
    "platforms": [],  # 限制平台1app2pc4小程序
    "promotionIds": [],  # 活动id集合
    "receiveRemarks": "",  # 领券说明(目前只在领取中心展示)
    "remarks": "",  # 说明
    "serialNos": [],  # 可用商品集合
    "stackTimes": 0,  # 叠加上限(null不限制)
    "startTime": "",  # 生效时间
    "startType": 0,  # 开始生效方式1定时生效2派发后生效
    "transferable": False,  # 是否支持顾客转赠 true:支持  false:不支持
    "transferableLimitCustomer": 0,  # C端转赠对象限制：1-所有顾客,2-自定义顾客群
    "useRange": 0,  # 使用范围:1-所有产品,2-指定产品,3-指定不适用产品,4-指定产品分类,5-指定活动6-指定签约购3.0活动,7-签约购4.0活动
    "usedCount": 0,  # 已核销数量
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
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
    - memberCustom.cardEndDate: 办卡月份止(yyyy-MM)
    - memberCustom.cardStartDate: 办卡月份起(yyyy-MM)
    - memberCustom.cardStatuses: 会员卡状态:-3.未开卡,-2.未升级,-1.待激活,0.有效,1.已失效,2.已注销
    - memberCustom.hyqEndDate: 限制限制会有趣账号注册时间止(yyyy-MM-dd)
    - memberCustom.hyqStartDate: 限制限制会有趣账号注册时间起(yyyy-MM-dd)
    - memberCustom.limitCardAfter: 办卡后参加资格：0-不限制，N-具体月
    - memberCustom.limitCardBefore: 过往办卡月份资格限制：0-不限制，N-具体月
    - memberCustom.limitCardDate: 限制办卡月份:0-不限制,1-限制,2-仅当月新开卡
    - memberCustom.limitHyqAccount: 是否限制会有趣账号: 0-不限制，1-限制
    - memberCustom.limitHyqDate: 是否限制会有趣账号注册时间: 0-不限制，1-限制
    - memberCustom.limitLoginDate: 限制访问时间:0-不限制,1-限制
    - memberCustom.limitMemberLevel: 是否限制顾客等级
    - memberCustom.limitOrderDate: 限制活跃月份(300pv):0-不限制,1-限制,2-从未活跃
    - memberCustom.limitPurchaseDate: 限制购货月份(1pv)：0-不限制，N-具体的累计月份
    - memberCustom.limitRegDate: 限制注册月份:0-不限制,1-限制
    - memberCustom.limitUpgradeDate: 限制升级月份:0-不限制,1-限制
    - memberCustom.limitWx: 是否限制企微好友：0-不限制，1-限制
    - memberCustom.limitWxDate: 是否限制企微加好友时间：0-不限制，1-限制
    - memberCustom.loginEndDate: 访问时间止(yyyy-MM)
    - memberCustom.loginPlatforms: 登录渠道:1-APP,2-PC,4-小程序
    - memberCustom.loginStartDate: 访问时间起(yyyy-MM)
    - memberCustom.memberLevels: 顾客等级:0.新用户,1.一星优惠客户,2.二星优惠客户,3.三星优惠客户,4.四星优惠客户,5.客户代表,6.客户经理,7.中级客户经理,8.客户总监,9.高级客户总监,10.资深客户总监,11.客户总经理
    - memberCustom.memberTypes: 顾客身份:1-普通顾客，2-优惠顾客，3-云商，4-微店
    - memberCustom.orderEndDate: 活跃月份止(yyyy-MM)
    - memberCustom.orderStartDate: 活跃月份起(yyyy-MM)
    - memberCustom.provinceCodes: 限制企微经销商省份Code集合
    - memberCustom.regEndDate: 注册月份止(yyyy-MM)
    - memberCustom.regStartDate: 注册月份起(yyyy-MM)
    - memberCustom.upgradeEndDate: 升级月份止(yyyy-MM)
    - memberCustom.upgradeStartDate: 升级月份起(yyyy-MM)
    - memberCustom.wxEndDate: 限制企微加好友时间止(yyyy-MM-dd)
    - memberCustom.wxStartDate: 限制企微加好友时间起(yyyy-MM-dd)
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

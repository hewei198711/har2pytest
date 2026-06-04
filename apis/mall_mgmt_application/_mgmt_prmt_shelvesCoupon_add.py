import os

from util.client import client

data = {
    "couponId": 0,  # 优惠券id
    "couponShowProducts": [],  # 优惠券卡片自定义关联商品集合
    "couponShowType": 0,  # 优惠券卡片推荐产品类型：0-默认，1-自定义关联
    "id": 0,  # 主键
    "importKey": "",  # 导入操作键:通过名单导入上架对象的导入操作key
    "limitCount": 0,  # 领取数量
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
    },  # 自定义顾客群(上架对象)
    "offShelves": 0,  # 下架方式:1-定时下架,2-不自动下架,3-领取完直接下架
    "offShelvesTime": "",  # 下架时间
    "platforms": [],  # 上架平台:1-APP,2-PC,4-小程序
    "receiveCount": 0,  # 领取总量
    "receiveMemberCustom": {
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
    },  # 自定义顾客群(领取对象)
    "receiveTarget": 0,  # 领取对象:1-所有顾客,2-自定义顾客群,4-通过名单导入
    "shelves": 0,  # 上架方式:1-定时上架,2-即时上架
    "shelvesChannels": [],  # 上架入口:1-商品详情,2-领券中心
    "shelvesTarget": 0,  # 上架对象:1-所有顾客,2-自定义顾客群,4-通过名单导入
    "shelvesTime": "",  # 上架时间
    "showOrder": 0,  # 展示顺序
    "state": 0,  # 状态:1-待审核,5-草稿
    "unlimitedReceiveCount": False,  # 是否不限制领取总量
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_shelvesCoupon_add(data=data, headers=headers):
    """
    新增优惠券上架记录
    /mgmt/prmt/shelvesCoupon/add

    参数说明:
    - couponId: 优惠券id
    - couponShowProducts: 优惠券卡片自定义关联商品集合
    - couponShowType: 优惠券卡片推荐产品类型：0-默认，1-自定义关联
    - id: 主键
    - importKey: 导入操作键:通过名单导入上架对象的导入操作key
    - limitCount: 领取数量
    - memberCustom: 自定义顾客群(上架对象)
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
    - offShelves: 下架方式:1-定时下架,2-不自动下架,3-领取完直接下架
    - offShelvesTime: 下架时间
    - platforms: 上架平台:1-APP,2-PC,4-小程序
    - receiveCount: 领取总量
    - receiveMemberCustom: 自定义顾客群(领取对象)
    - receiveMemberCustom.cardEndDate: 办卡月份止(yyyy-MM)
    - receiveMemberCustom.cardStartDate: 办卡月份起(yyyy-MM)
    - receiveMemberCustom.cardStatuses: 会员卡状态:-3.未开卡,-2.未升级,-1.待激活,0.有效,1.已失效,2.已注销
    - receiveMemberCustom.hyqEndDate: 限制限制会有趣账号注册时间止(yyyy-MM-dd)
    - receiveMemberCustom.hyqStartDate: 限制限制会有趣账号注册时间起(yyyy-MM-dd)
    - receiveMemberCustom.limitCardAfter: 办卡后参加资格：0-不限制，N-具体月
    - receiveMemberCustom.limitCardBefore: 过往办卡月份资格限制：0-不限制，N-具体月
    - receiveMemberCustom.limitCardDate: 限制办卡月份:0-不限制,1-限制,2-仅当月新开卡
    - receiveMemberCustom.limitHyqAccount: 是否限制会有趣账号: 0-不限制，1-限制
    - receiveMemberCustom.limitHyqDate: 是否限制会有趣账号注册时间: 0-不限制，1-限制
    - receiveMemberCustom.limitLoginDate: 限制访问时间:0-不限制,1-限制
    - receiveMemberCustom.limitMemberLevel: 是否限制顾客等级
    - receiveMemberCustom.limitOrderDate: 限制活跃月份(300pv):0-不限制,1-限制,2-从未活跃
    - receiveMemberCustom.limitPurchaseDate: 限制购货月份(1pv)：0-不限制，N-具体的累计月份
    - receiveMemberCustom.limitRegDate: 限制注册月份:0-不限制,1-限制
    - receiveMemberCustom.limitUpgradeDate: 限制升级月份:0-不限制,1-限制
    - receiveMemberCustom.limitWx: 是否限制企微好友：0-不限制，1-限制
    - receiveMemberCustom.limitWxDate: 是否限制企微加好友时间：0-不限制，1-限制
    - receiveMemberCustom.loginEndDate: 访问时间止(yyyy-MM)
    - receiveMemberCustom.loginPlatforms: 登录渠道:1-APP,2-PC,4-小程序
    - receiveMemberCustom.loginStartDate: 访问时间起(yyyy-MM)
    - receiveMemberCustom.memberLevels: 顾客等级:0.新用户,1.一星优惠客户,2.二星优惠客户,3.三星优惠客户,4.四星优惠客户,5.客户代表,6.客户经理,7.中级客户经理,8.客户总监,9.高级客户总监,10.资深客户总监,11.客户总经理
    - receiveMemberCustom.memberTypes: 顾客身份:1-普通顾客，2-优惠顾客，3-云商，4-微店
    - receiveMemberCustom.orderEndDate: 活跃月份止(yyyy-MM)
    - receiveMemberCustom.orderStartDate: 活跃月份起(yyyy-MM)
    - receiveMemberCustom.provinceCodes: 限制企微经销商省份Code集合
    - receiveMemberCustom.regEndDate: 注册月份止(yyyy-MM)
    - receiveMemberCustom.regStartDate: 注册月份起(yyyy-MM)
    - receiveMemberCustom.upgradeEndDate: 升级月份止(yyyy-MM)
    - receiveMemberCustom.upgradeStartDate: 升级月份起(yyyy-MM)
    - receiveMemberCustom.wxEndDate: 限制企微加好友时间止(yyyy-MM-dd)
    - receiveMemberCustom.wxStartDate: 限制企微加好友时间起(yyyy-MM-dd)
    - receiveTarget: 领取对象:1-所有顾客,2-自定义顾客群,4-通过名单导入
    - shelves: 上架方式:1-定时上架,2-即时上架
    - shelvesChannels: 上架入口:1-商品详情,2-领券中心
    - shelvesTarget: 上架对象:1-所有顾客,2-自定义顾客群,4-通过名单导入
    - shelvesTime: 上架时间
    - showOrder: 展示顺序
    - state: 状态:1-待审核,5-草稿
    - unlimitedReceiveCount: 是否不限制领取总量
    """

    url = "/mgmt/prmt/shelvesCoupon/add"
    with client.post(url=url, json=data, headers=headers) as r:
        return r

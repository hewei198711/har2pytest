import os

from util.client import client

data = {
    "cardStatuses": [],  # TODO: 添加参数说明
    "couponId": 0,  # 优惠券id
    "endTime": "",  # TODO: 添加参数说明
    "everyCount": 0,  # 每人发放数量
    "fixedTime": "",  # 定时派发时间(yyyy-MM-dd HH:mm:ss)
    "grantEndTime": "",  # 定时派发结束时间(yyyy-MM-dd HH:mm:ss)
    "grantStartTime": "",  # 定时派发开始时间(yyyy-MM-dd HH:mm:ss)
    "grantTarget": 0,  # 派发对象1所有人2身份3等级4导入
    "grantType": 0,  # 派发方式:1-即时派发,2-定时派发,3-每日循环派发,4-每月定时派发,5-对接外部系统,6-对接企微系统
    "id": 0,  # 派发记录id
    "importKey": "",  # 导入操作键
    "limitCardTime": 0,  # TODO: 添加参数说明
    "limitMemberLevel": False,  # TODO: 添加参数说明
    "limitOrderTime": 0,  # TODO: 添加参数说明
    "limitRegTime": 0,  # TODO: 添加参数说明
    "limitUseCoupon": False,  # 派发对象使用限制：false-否，true-是
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
    "memberIdentities": [],  # 用户身份集合
    "memberLevelList": [],  # TODO: 添加参数说明
    "orderEndTime": "",  # TODO: 添加参数说明
    "orderStartTime": "",  # TODO: 添加参数说明
    "regEndTime": "",  # TODO: 添加参数说明
    "regStartTime": "",  # TODO: 添加参数说明
    "remark": "",  # 派发说明
    "startTime": "",  # TODO: 添加参数说明
    "state": 0,  # 发放状态1待审核2派发中3已完成4已驳回5草稿
    "type": 0,  # 导入方式1等量派发2按需派发
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_couponGrant_editCouponGrant(data=data, headers=headers):
    """
    编辑优惠券派发记录
    /mgmt/prmt/couponGrant/editCouponGrant

    参数说明:
    - couponId: 优惠券id
    - everyCount: 每人发放数量
    - fixedTime: 定时派发时间(yyyy-MM-dd HH:mm:ss)
    - grantEndTime: 定时派发结束时间(yyyy-MM-dd HH:mm:ss)
    - grantStartTime: 定时派发开始时间(yyyy-MM-dd HH:mm:ss)
    - grantTarget: 派发对象1所有人2身份3等级4导入
    - grantType: 派发方式:1-即时派发,2-定时派发,3-每日循环派发,4-每月定时派发,5-对接外部系统,6-对接企微系统
    - id: 派发记录id
    - importKey: 导入操作键
    - limitUseCoupon: 派发对象使用限制：false-否，true-是
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
    - memberIdentities: 用户身份集合
    - remark: 派发说明
    - state: 发放状态1待审核2派发中3已完成4已驳回5草稿
    - type: 导入方式1等量派发2按需派发
    """

    url = "/mgmt/prmt/couponGrant/editCouponGrant"
    with client.post(url=url, json=data, headers=headers) as r:
        return r

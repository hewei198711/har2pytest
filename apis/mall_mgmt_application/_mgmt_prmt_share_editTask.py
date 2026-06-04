import os

from util.client import client

data = {
    "assistCount": 0,  # 助力人数
    "assistCouponId": 0,  # 助力可获得优惠券id
    "assistCouponShowProducts": [],  # 助力人优惠券卡片自定义关联商品集合
    "assistCouponShowType": 0,  # 助力人优惠券卡片推荐产品类型：0-默认，1-自定义关联
    "assistEveryCount": 0,  # 每次助力领取数量
    "assistGetCount": 0,  # 助力人领取总量(-1不限制)
    "assistGetCoupon": False,  # 助力是否获券false否true是
    "assistLimitCustomer": 0,  # 助力对象1所有2身份
    "assistMemberCustom": {
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
    },  # 助力人自定义顾客群
    "assistTimes": 0,  # 助力次数
    "expireTimeHour": 0,  # 任务有效期(时)
    "expireTimeMinute": 0,  # 任务有效期(分)
    "getMoment": 0,  # 领取节点1参与助力领券2完成任务领券
    "getWay": 0,  # 领取入口1领券中心
    "id": 0,  # TODO: 添加参数说明
    "importKey": "",  # 导入操作键
    "limitAssistGetCount": False,  # 是否限制助力人领取总量
    "limitAssistTimes": False,  # 是否限制助力次数
    "limitShareCount": False,  # 是否限制发起活动次数
    "limitShareGetCount": False,  # 是否限制分享人领取总量
    "offShelfTime": "",  # 下架时间
    "offShelfType": 0,  # 下架方式1定时下架2不自动下架3领取完直接下架
    "onShelfTime": "",  # 上架时间
    "onShelfType": 0,  # 上架方式1定时上架2即时上架
    "remarks": "",  # 活动说明
    "shareCount": 0,  # 发起活动次数(-1不限制)
    "shareCouponId": 0,  # 分享可获得优惠券id
    "shareCouponShowProducts": [],  # 分享人优惠券卡片自定义关联商品集合
    "shareCouponShowType": 0,  # 分享人优惠券卡片推荐产品类型：0-默认，1-自定义关联
    "shareEveryCount": 0,  # 每次任务领取数量
    "shareGetCount": 0,  # 分享人领取总量(-1不限制)
    "shareLimitCustomer": 0,  # 领取对象1所有2身份4导入
    "shareMemberCustom": {
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
    },  # 分享人自定义顾客群
    "sharePicture": "",  # 分享推广图地址
    "sharerAssist": False,  # 分享人是否可助力
    "shelfPlatforms": [],  # 上架平台1app2pc4小程序
    "showOrder": 0,  # 展示顺序
    "taskName": "",  # 活动名称
    "taskState": 0,  # 任务状态1待审核2待上架3已上架4已下架5已驳回6草稿
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_share_editTask(data=data, headers=headers):
    """
    编辑分享领券活动
    /mgmt/prmt/share/editTask

    参数说明:
    - assistCount: 助力人数
    - assistCouponId: 助力可获得优惠券id
    - assistCouponShowProducts: 助力人优惠券卡片自定义关联商品集合
    - assistCouponShowType: 助力人优惠券卡片推荐产品类型：0-默认，1-自定义关联
    - assistEveryCount: 每次助力领取数量
    - assistGetCount: 助力人领取总量(-1不限制)
    - assistGetCoupon: 助力是否获券false否true是
    - assistLimitCustomer: 助力对象1所有2身份
    - assistMemberCustom: 助力人自定义顾客群
    - assistMemberCustom.cardEndDate: 办卡月份止(yyyy-MM)
    - assistMemberCustom.cardStartDate: 办卡月份起(yyyy-MM)
    - assistMemberCustom.cardStatuses: 会员卡状态:-3.未开卡,-2.未升级,-1.待激活,0.有效,1.已失效,2.已注销
    - assistMemberCustom.hyqEndDate: 限制限制会有趣账号注册时间止(yyyy-MM-dd)
    - assistMemberCustom.hyqStartDate: 限制限制会有趣账号注册时间起(yyyy-MM-dd)
    - assistMemberCustom.limitCardAfter: 办卡后参加资格：0-不限制，N-具体月
    - assistMemberCustom.limitCardBefore: 过往办卡月份资格限制：0-不限制，N-具体月
    - assistMemberCustom.limitCardDate: 限制办卡月份:0-不限制,1-限制,2-仅当月新开卡
    - assistMemberCustom.limitHyqAccount: 是否限制会有趣账号: 0-不限制，1-限制
    - assistMemberCustom.limitHyqDate: 是否限制会有趣账号注册时间: 0-不限制，1-限制
    - assistMemberCustom.limitLoginDate: 限制访问时间:0-不限制,1-限制
    - assistMemberCustom.limitMemberLevel: 是否限制顾客等级
    - assistMemberCustom.limitOrderDate: 限制活跃月份(300pv):0-不限制,1-限制,2-从未活跃
    - assistMemberCustom.limitPurchaseDate: 限制购货月份(1pv)：0-不限制，N-具体的累计月份
    - assistMemberCustom.limitRegDate: 限制注册月份:0-不限制,1-限制
    - assistMemberCustom.limitUpgradeDate: 限制升级月份:0-不限制,1-限制
    - assistMemberCustom.limitWx: 是否限制企微好友：0-不限制，1-限制
    - assistMemberCustom.limitWxDate: 是否限制企微加好友时间：0-不限制，1-限制
    - assistMemberCustom.loginEndDate: 访问时间止(yyyy-MM)
    - assistMemberCustom.loginPlatforms: 登录渠道:1-APP,2-PC,4-小程序
    - assistMemberCustom.loginStartDate: 访问时间起(yyyy-MM)
    - assistMemberCustom.memberLevels: 顾客等级:0.新用户,1.一星优惠客户,2.二星优惠客户,3.三星优惠客户,4.四星优惠客户,5.客户代表,6.客户经理,7.中级客户经理,8.客户总监,9.高级客户总监,10.资深客户总监,11.客户总经理
    - assistMemberCustom.memberTypes: 顾客身份:1-普通顾客，2-优惠顾客，3-云商，4-微店
    - assistMemberCustom.orderEndDate: 活跃月份止(yyyy-MM)
    - assistMemberCustom.orderStartDate: 活跃月份起(yyyy-MM)
    - assistMemberCustom.provinceCodes: 限制企微经销商省份Code集合
    - assistMemberCustom.regEndDate: 注册月份止(yyyy-MM)
    - assistMemberCustom.regStartDate: 注册月份起(yyyy-MM)
    - assistMemberCustom.upgradeEndDate: 升级月份止(yyyy-MM)
    - assistMemberCustom.upgradeStartDate: 升级月份起(yyyy-MM)
    - assistMemberCustom.wxEndDate: 限制企微加好友时间止(yyyy-MM-dd)
    - assistMemberCustom.wxStartDate: 限制企微加好友时间起(yyyy-MM-dd)
    - assistTimes: 助力次数
    - expireTimeHour: 任务有效期(时)
    - expireTimeMinute: 任务有效期(分)
    - getMoment: 领取节点1参与助力领券2完成任务领券
    - getWay: 领取入口1领券中心
    - importKey: 导入操作键
    - limitAssistGetCount: 是否限制助力人领取总量
    - limitAssistTimes: 是否限制助力次数
    - limitShareCount: 是否限制发起活动次数
    - limitShareGetCount: 是否限制分享人领取总量
    - offShelfTime: 下架时间
    - offShelfType: 下架方式1定时下架2不自动下架3领取完直接下架
    - onShelfTime: 上架时间
    - onShelfType: 上架方式1定时上架2即时上架
    - remarks: 活动说明
    - shareCount: 发起活动次数(-1不限制)
    - shareCouponId: 分享可获得优惠券id
    - shareCouponShowProducts: 分享人优惠券卡片自定义关联商品集合
    - shareCouponShowType: 分享人优惠券卡片推荐产品类型：0-默认，1-自定义关联
    - shareEveryCount: 每次任务领取数量
    - shareGetCount: 分享人领取总量(-1不限制)
    - shareLimitCustomer: 领取对象1所有2身份4导入
    - shareMemberCustom: 分享人自定义顾客群
    - shareMemberCustom.cardEndDate: 办卡月份止(yyyy-MM)
    - shareMemberCustom.cardStartDate: 办卡月份起(yyyy-MM)
    - shareMemberCustom.cardStatuses: 会员卡状态:-3.未开卡,-2.未升级,-1.待激活,0.有效,1.已失效,2.已注销
    - shareMemberCustom.hyqEndDate: 限制限制会有趣账号注册时间止(yyyy-MM-dd)
    - shareMemberCustom.hyqStartDate: 限制限制会有趣账号注册时间起(yyyy-MM-dd)
    - shareMemberCustom.limitCardAfter: 办卡后参加资格：0-不限制，N-具体月
    - shareMemberCustom.limitCardBefore: 过往办卡月份资格限制：0-不限制，N-具体月
    - shareMemberCustom.limitCardDate: 限制办卡月份:0-不限制,1-限制,2-仅当月新开卡
    - shareMemberCustom.limitHyqAccount: 是否限制会有趣账号: 0-不限制，1-限制
    - shareMemberCustom.limitHyqDate: 是否限制会有趣账号注册时间: 0-不限制，1-限制
    - shareMemberCustom.limitLoginDate: 限制访问时间:0-不限制,1-限制
    - shareMemberCustom.limitMemberLevel: 是否限制顾客等级
    - shareMemberCustom.limitOrderDate: 限制活跃月份(300pv):0-不限制,1-限制,2-从未活跃
    - shareMemberCustom.limitPurchaseDate: 限制购货月份(1pv)：0-不限制，N-具体的累计月份
    - shareMemberCustom.limitRegDate: 限制注册月份:0-不限制,1-限制
    - shareMemberCustom.limitUpgradeDate: 限制升级月份:0-不限制,1-限制
    - shareMemberCustom.limitWx: 是否限制企微好友：0-不限制，1-限制
    - shareMemberCustom.limitWxDate: 是否限制企微加好友时间：0-不限制，1-限制
    - shareMemberCustom.loginEndDate: 访问时间止(yyyy-MM)
    - shareMemberCustom.loginPlatforms: 登录渠道:1-APP,2-PC,4-小程序
    - shareMemberCustom.loginStartDate: 访问时间起(yyyy-MM)
    - shareMemberCustom.memberLevels: 顾客等级:0.新用户,1.一星优惠客户,2.二星优惠客户,3.三星优惠客户,4.四星优惠客户,5.客户代表,6.客户经理,7.中级客户经理,8.客户总监,9.高级客户总监,10.资深客户总监,11.客户总经理
    - shareMemberCustom.memberTypes: 顾客身份:1-普通顾客，2-优惠顾客，3-云商，4-微店
    - shareMemberCustom.orderEndDate: 活跃月份止(yyyy-MM)
    - shareMemberCustom.orderStartDate: 活跃月份起(yyyy-MM)
    - shareMemberCustom.provinceCodes: 限制企微经销商省份Code集合
    - shareMemberCustom.regEndDate: 注册月份止(yyyy-MM)
    - shareMemberCustom.regStartDate: 注册月份起(yyyy-MM)
    - shareMemberCustom.upgradeEndDate: 升级月份止(yyyy-MM)
    - shareMemberCustom.upgradeStartDate: 升级月份起(yyyy-MM)
    - shareMemberCustom.wxEndDate: 限制企微加好友时间止(yyyy-MM-dd)
    - shareMemberCustom.wxStartDate: 限制企微加好友时间起(yyyy-MM-dd)
    - sharePicture: 分享推广图地址
    - sharerAssist: 分享人是否可助力
    - shelfPlatforms: 上架平台1app2pc4小程序
    - showOrder: 展示顺序
    - taskName: 活动名称
    - taskState: 任务状态1待审核2待上架3已上架4已下架5已驳回6草稿
    """

    url = "/mgmt/prmt/share/editTask"
    with client.post(url=url, json=data, headers=headers) as r:
        return r

import os

from util.client import client

data = {
    "activityName": "",  # 活动名称
    "appReceivingPage": 0,  # app提醒页面提醒位置:0-首页 1-购物车 2-我的 3-赚金豆 4-我的展业 5-直播列表
    "couponList": [{"couponId": 0, "getCount": 0}],  # 关联优惠券
    "endTime": "",  # 结束时间
    "externalLink": "",  # 外部链接
    "frequency": 0,  # 提醒频次:0-每次访问提醒,1-每日提醒1次,2-每月提醒1次
    "giveCoupon": False,  # 登录送券:true-送券,false-不送券
    "id": 0,  # 登录有礼记录主键
    "importKey": "",  # 导入操作键:自由导入活动对象的导入操作key
    "luckyList": [],  # 关联抽奖活动id列表
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
    "opportunity": 0,  # 提醒&送券时机:0-即时提醒,1-生日提醒,2-办卡周年提醒,3-会员卡即将失效提醒,4-会员卡过期提醒
    "opportunityDelay": 0,  # 提醒时机延时配置-即时提醒(单位:秒)
    "participants": 0,  # 活动对象:1-所有顾客,2-顾客身份,4-自由导入
    "pathApp": "",  # app端链接地址
    "pathAppType": 0,  # app端链类型(关联类型为内/外部链接时才使用)：1-内部,2-外部
    "pathMiniProgram": "",  # 小程序端链接地址
    "pathMiniProgramType": 0,  # 小程序端链接类型(关联类型为内/外部链接时才使用)：1-内部,2-外部
    "pathPc": "",  # pc端链接地址
    "pathPcType": 0,  # pc端链接类型(关联类型为内/外部链接时才使用)：1-内部,2-外部
    "pcReceivingPage": 0,  # pc提醒页面提醒位置:0-首页 1-购物车 2-我的 3-赚金豆 4-我的展业 5-直播列表
    "platforms": [],  # 领券平台:1-APP,2-PC,4-小程序
    "posterPic": "",  # 海报
    "posterRelation": 0,  # 海报关联:0-无,1-关联产品,2-关联外部链接,3-关联抽奖活动,4-关联问卷,5-关联内部链接,6-关联签约购2.0活动7-关联签约购3.0活动,8-关联专区页面,9-关联抢购活动,10-关联随心购活动,11-关联随心购活动列表,12-关联3S活动,13-关联链接(指定内/外部链接)14-关联签约购4.0活动, 15-关联签约购4.0活动列表, 16-送礼活动
    "productList": [{"serialNo": "", "title": ""}],  # 关联产品列表
    "projectKey": "",  # 问卷projectKey
    "promotionId": 0,  # 签约购2.0活动id, 签约购3.0活动id, 专区活动页面id, 抢购活动id, 随心购活动id, 3S活动id, 签约购4.0活动id, 送礼活动id
    "remarks": "",  # 活动说明
    "remind": False,  # 是否登录提醒
    "startTime": "",  # 开始时间
    "status": 0,  # 状态:1-待审核,2-进行中,3-已完成,4-已驳回,5-草稿,6-已停止
    "unlimitedTime": False,  # 是否不限时
    "wxReceivingPage": 0,  # 小程序提醒页面提醒位置:0-首页 1-购物车 2-我的 3-赚金豆 4-我的展业 5-直播列表
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_loginGift_editLoginGift(data=data, headers=headers):
    """
    编辑登录有礼活动
    /mgmt/prmt/loginGift/editLoginGift

    参数说明:
    - activityName: 活动名称
    - appReceivingPage: app提醒页面提醒位置:0-首页 1-购物车 2-我的 3-赚金豆 4-我的展业 5-直播列表
    - couponList: 关联优惠券
    - couponList.couponId: 优惠券id
    - couponList.getCount: 派发数量
    - endTime: 结束时间
    - externalLink: 外部链接
    - frequency: 提醒频次:0-每次访问提醒,1-每日提醒1次,2-每月提醒1次
    - giveCoupon: 登录送券:true-送券,false-不送券
    - id: 登录有礼记录主键
    - importKey: 导入操作键:自由导入活动对象的导入操作key
    - luckyList: 关联抽奖活动id列表
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
    - opportunity: 提醒&送券时机:0-即时提醒,1-生日提醒,2-办卡周年提醒,3-会员卡即将失效提醒,4-会员卡过期提醒
    - opportunityDelay: 提醒时机延时配置-即时提醒(单位:秒)
    - participants: 活动对象:1-所有顾客,2-顾客身份,4-自由导入
    - pathApp: app端链接地址
    - pathAppType: app端链类型(关联类型为内/外部链接时才使用)：1-内部,2-外部
    - pathMiniProgram: 小程序端链接地址
    - pathMiniProgramType: 小程序端链接类型(关联类型为内/外部链接时才使用)：1-内部,2-外部
    - pathPc: pc端链接地址
    - pathPcType: pc端链接类型(关联类型为内/外部链接时才使用)：1-内部,2-外部
    - pcReceivingPage: pc提醒页面提醒位置:0-首页 1-购物车 2-我的 3-赚金豆 4-我的展业 5-直播列表
    - platforms: 领券平台:1-APP,2-PC,4-小程序
    - posterPic: 海报
    - posterRelation: 海报关联:0-无,1-关联产品,2-关联外部链接,3-关联抽奖活动,4-关联问卷,5-关联内部链接,6-关联签约购2.0活动7-关联签约购3.0活动,8-关联专区页面,9-关联抢购活动,10-关联随心购活动,11-关联随心购活动列表,12-关联3S活动,13-关联链接(指定内/外部链接)14-关联签约购4.0活动, 15-关联签约购4.0活动列表, 16-送礼活动
    - productList: 关联产品列表
    - productList.serialNo: 商品编码
    - productList.title: 商品名
    - projectKey: 问卷projectKey
    - promotionId: 签约购2.0活动id, 签约购3.0活动id, 专区活动页面id, 抢购活动id, 随心购活动id, 3S活动id, 签约购4.0活动id, 送礼活动id
    - remarks: 活动说明
    - remind: 是否登录提醒
    - startTime: 开始时间
    - status: 状态:1-待审核,2-进行中,3-已完成,4-已驳回,5-草稿,6-已停止
    - unlimitedTime: 是否不限时
    - wxReceivingPage: 小程序提醒页面提醒位置:0-首页 1-购物车 2-我的 3-赚金豆 4-我的展业 5-直播列表
    """

    url = "/mgmt/prmt/loginGift/editLoginGift"
    with client.post(url=url, json=data, headers=headers) as r:
        return r

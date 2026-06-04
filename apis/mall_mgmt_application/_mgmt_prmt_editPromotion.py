import os

from util.client import client

data = {
    "configDto": {
        "appPosterImg": "",
        "day": 0,
        "exchangeType": 0,
        "hour": 0,
        "id": 0,
        "independentLimit": 0,
        "isNotice": 0,
        "limitCustomer": 0,
        "limitNumber": 0,
        "limitProduct": 0,
        "limitTimes": 0,
        "limitTimesType": 0,
        "limitType": 0,
        "minute": 0,
        "noticeContent": 0,
        "noticeTime": "",
        "payLimitTime": 0,
        "payMinute": 0,
        "pcPosterImg": "",
        "showEndTime": 0,
        "takePartLimitTimes": 0,
    },  # 活动配置
    "couponIds": [],  # 优惠券id集合
    "customDays": 0,  # 定金支付时效自定义(天)
    "customHours": 0,  # 定金支付时效自定义(时)
    "customMinutes": 0,  # 定金支付时效自定义(分)
    "endTime": "",  # 结束时间
    "expireOption": 0,  # 定金支付时效配置项:0-自定义,1-15分钟,2-30分钟,3-1小时
    "getCounts": [],  # 可购买数量集合（阶梯统一限量时使用）
    "id": 0,  # 活动id
    "importKey": "",  # 导入操作键
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
    "payEndTime": "",  # 尾款支付结束时间
    "payStartTime": "",  # 尾款支付开始时间
    "pointSteps": [],  # 活动PV阶梯集合
    "productDtos": [
        {"deliveryDate": "", "getCounts": [], "id": 0, "originalPrice": 0.0, "productName": "", "serialNo": ""}
    ],  # 活动产品集合
    "promotionCode": "",  # 活动编号
    "promotionName": "",  # 活动名称
    "promotionState": 0,  # 活动状态1待审核2待开始3进行中4已结束5已驳回6草稿
    "promotionType": 0,  # 活动类型:1-活动,2-换购,4-预售
    "promotionTypeExt": 0,  # 基于抢购活动(promotionType=1)类型区分：0-原抢购(秒杀) 1-常规
    "remarks": "",  # 活动说明
    "serialNos": [],  # 换购需加购产品编码集合
    "startTime": "",  # 开始时间
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_editPromotion(data=data, headers=headers):
    """
    编辑活动
    /mgmt/prmt/editPromotion

    参数说明:
    - configDto: 活动配置
    - configDto.appPosterImg: APP海报图片
    - configDto.day: 天
    - configDto.exchangeType: 换购类型1产品换购2PV达标换购3数量达标换购4金额达标换购
    - configDto.hour: 时
    - configDto.id: id
    - configDto.independentLimit: 自定义独立限量1:开启;0:关闭
    - configDto.isNotice: 是否预告0预告1不预告
    - configDto.limitCustomer: 参与顾客设置1所有2顾客身份3顾客等级4导入
    - configDto.limitNumber: 限购数量(-1不限,-2按需分配)
    - configDto.limitProduct: 限制换购主产品方式1全部产品2指定产品
    - configDto.limitTimes: 限购次数(换购活动)
    - configDto.limitTimesType: 换购活动限制购买商品次数类型(-1:不限次数, 0:限制次数, 1:限制次数(自然月))
    - configDto.limitType: 限购方式1不限量2独立限量3统一限量4按需导入5按阶梯配置独立限量6按阶梯配置统一限量
    - configDto.minute: 分
    - configDto.noticeContent: 预告内容1产品2海报
    - configDto.noticeTime: 预告时间
    - configDto.payLimitTime: 1跟随系统，2自定义
    - configDto.payMinute: 换算后分
    - configDto.pcPosterImg: PC海报图片
    - configDto.showEndTime: 是否显示结束时间0否1是
    - configDto.takePartLimitTimes: 常规活动限制参与次数(0-不限制,N-具体的限制次数)
    - couponIds: 优惠券id集合
    - customDays: 定金支付时效自定义(天)
    - customHours: 定金支付时效自定义(时)
    - customMinutes: 定金支付时效自定义(分)
    - endTime: 结束时间
    - expireOption: 定金支付时效配置项:0-自定义,1-15分钟,2-30分钟,3-1小时
    - getCounts: 可购买数量集合（阶梯统一限量时使用）
    - id: 活动id
    - importKey: 导入操作键
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
    - payEndTime: 尾款支付结束时间
    - payStartTime: 尾款支付开始时间
    - pointSteps: 活动PV阶梯集合
    - productDtos: 活动产品集合
    - productDtos.deliveryDate: 预计发货时间
    - productDtos.getCounts: 可购买数量集合
    - productDtos.id: id:手动新增为活动id，编辑为行记录id
    - productDtos.originalPrice: 原价
    - productDtos.productName: 产品名称
    - productDtos.serialNo: 产品编码
    - promotionCode: 活动编号
    - promotionName: 活动名称
    - promotionState: 活动状态1待审核2待开始3进行中4已结束5已驳回6草稿
    - promotionType: 活动类型:1-活动,2-换购,4-预售
    - promotionTypeExt: 基于抢购活动(promotionType=1)类型区分：0-原抢购(秒杀) 1-常规
    - remarks: 活动说明
    - serialNos: 换购需加购产品编码集合
    - startTime: 开始时间
    """

    url = "/mgmt/prmt/editPromotion"
    with client.post(url=url, json=data, headers=headers) as r:
        return r

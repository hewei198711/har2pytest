import os

from util.client import client

data = {
    "activityCode": "",  # 活动编号
    "activityId": 0,  # 活动ID,判断新增/编辑的依据
    "activityName": "",  # 活动名称
    "addCounts1s": 0,  # 每次分享/助力增加的次数
    "centerPicture": "",  # 活动中心展示图
    "consumeBean": 0,  # 每次抽奖消耗金豆数量
    "customerType": 0,  # 顾客类型(1:所有顾客；2:自定义；4:自由导入)
    "endTime": "",  # 活动结束时间 2222-01-01 等于不自动结束
    "endTipsContent": "",  # 其它配置-活动结束提示(文字内容或图片地址)
    "endTipsType": 0,  # 其它配置-活动结束提示类型 0-文字，1-图片
    "hideUnwinStatus": 0,  # 前台隐藏未中奖信息 1、开启  2、关闭
    "importKey": "",  # 导入商品操作键
    "isShareAddCounts": 0,  # 是否分享增加次数(0-否 1-分享活动页面 2-分享活动并得到助力)
    "isShowLuckyList": 0,  # 是否展示中奖名单(0:否；1;是)
    "limitType": 0,  # 抽奖条件(0:无门槛 1-满PV)
    "limitTypeValue": 0,  # 抽奖限制条件数值
    "luckyCounts": 0,  # 抽奖次数
    "luckyCountsType": 0,  # 抽奖次数类型(0-每天次数，1-总次数，2-最大抽奖次数)
    "luckyPosition": 0,  # 抽奖位
    "luckyResultType": 0,  # 前台抽奖结果样式：0-常规抽奖结果样式  1-刮刮乐抽奖结果样式
    "maxShareCounts1d": 0,  # 每天最多分享次数/最多可被助力次数
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
    "openBean": 0,  # 消耗金豆抽奖：0-关闭 1-开启
    "passwordCode": "",  # 口令活动编码
    "passwordId": 0,  # 口令活动id
    "passwordName": "",  # 口令活动名称
    "pcBackgroundPicture": "",  # pc活动背景图
    "plateConfigList": [
        {"activityId": 0, "luckyRate": 0.0, "npId": 0, "plateId": 0, "positionNumber": 0, "prizeId": 0}
    ],  # 奖盘配置activityId必填,prizeId 和 npId其中一个不能是空
    "prizePlateStyle": 0,  # 奖盘样式(1-大转盘 2-盲盒)
    "prmtNotPrizeConfigDTO": {
        "activityId": 0,
        "blindBoxRemark": "",
        "couponId": 0,
        "isGetCoupon": 0,
        "limitHandNumber": 0,
        "mobileRegion": "",
        "mobileResultPicture": "",
        "npId": 0,
        "pcRegion": "",
        "pcResultPicture": "",
        "prizeHandType": 0,
        "prizeName": "",
        "prizePicture": "",
        "tips": "",
    },  # 不中奖配置
    "prmtPrizeConfigList": [
        {
            "activityId": 0,
            "alreadyHandNumber": 0,
            "blindBoxRemark": "",
            "couponId": 0,
            "limitHandNumber": 0,
            "mobileRegion": "",
            "mobileResultPicture": "",
            "onceBeanAmount": 0,
            "pcRegion": "",
            "pcResultPicture": "",
            "prizeHandType": 0,
            "prizeId": 0,
            "prizeName": "",
            "prizePicture": "",
            "prizeType": 0,
            "sourceId": 0,
        }
    ],  # 奖品配置
    "productType": 0,  # pv抽奖商品配置类型：0-黑名单商品 1-白名单商品
    "remark": "",  # 活动说明
    "startTime": "",  # 活动开始时间
    "state": 0,  # 状态(1待审核2待开始3进行中4已结束5已驳回6草稿)
    "winningCounts": 0,  # 中奖次数
    "winningCountsType": 0,  # 中奖次数类型(0:不限次数；1:统一次数)
    "wxGuide": 0,  # 是否开启企微引导：0-否，1-是
    "wxGuidePicture": "",  # 企微引导图片地址
    "wxShareAssistPicture": "",  # 分享助力小程序分享卡片图
    "wxShareAssistRemark": "",  # 分享助力小程序分享卡片文案
    "wxSharePicture": "",  # 小程序分享卡片图
    "ydBackgroundPicture": "",  # yd活动背景图
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_luckyActivity_addBaseInfo(data=data, headers=headers):
    """
    抽奖活动-新增 步骤一
    /mgmt/prmt/luckyActivity/addBaseInfo

    参数说明:
    - activityCode: 活动编号
    - activityId: 活动ID,判断新增/编辑的依据
    - activityName: 活动名称
    - addCounts1s: 每次分享/助力增加的次数
    - centerPicture: 活动中心展示图
    - consumeBean: 每次抽奖消耗金豆数量
    - customerType: 顾客类型(1:所有顾客；2:自定义；4:自由导入)
    - endTime: 活动结束时间 2222-01-01 等于不自动结束
    - endTipsContent: 其它配置-活动结束提示(文字内容或图片地址)
    - endTipsType: 其它配置-活动结束提示类型 0-文字，1-图片
    - hideUnwinStatus: 前台隐藏未中奖信息 1、开启  2、关闭
    - importKey: 导入商品操作键
    - isShareAddCounts: 是否分享增加次数(0-否 1-分享活动页面 2-分享活动并得到助力)
    - isShowLuckyList: 是否展示中奖名单(0:否；1;是)
    - limitType: 抽奖条件(0:无门槛 1-满PV)
    - limitTypeValue: 抽奖限制条件数值
    - luckyCounts: 抽奖次数
    - luckyCountsType: 抽奖次数类型(0-每天次数，1-总次数，2-最大抽奖次数)
    - luckyPosition: 抽奖位
    - luckyResultType: 前台抽奖结果样式：0-常规抽奖结果样式  1-刮刮乐抽奖结果样式
    - maxShareCounts1d: 每天最多分享次数/最多可被助力次数
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
    - openBean: 消耗金豆抽奖：0-关闭 1-开启
    - passwordCode: 口令活动编码
    - passwordId: 口令活动id
    - passwordName: 口令活动名称
    - pcBackgroundPicture: pc活动背景图
    - plateConfigList: 奖盘配置activityId必填,prizeId 和 npId其中一个不能是空
    - plateConfigList.activityId: 活动id
    - plateConfigList.luckyRate: 抽奖概率
    - plateConfigList.npId: 不中奖配置id
    - plateConfigList.plateId: id标识
    - plateConfigList.positionNumber: 奖盘位置号
    - plateConfigList.prizeId: 奖品id
    - prizePlateStyle: 奖盘样式(1-大转盘 2-盲盒)
    - prmtNotPrizeConfigDTO: 不中奖配置
    - prmtNotPrizeConfigDTO.activityId: 活动id
    - prmtNotPrizeConfigDTO.blindBoxRemark: 盲盒模式不中奖奖品文案
    - prmtNotPrizeConfigDTO.couponId: 优惠券id
    - prmtNotPrizeConfigDTO.isGetCoupon: 是否获券(0:否;1:是)
    - prmtNotPrizeConfigDTO.limitHandNumber: 奖品限制派发数量
    - prmtNotPrizeConfigDTO.mobileRegion: 移动端刮刮乐区域配置
    - prmtNotPrizeConfigDTO.mobileResultPicture: 移动端抽奖结果图片地址(刮刮乐)
    - prmtNotPrizeConfigDTO.npId: 不中奖配置id
    - prmtNotPrizeConfigDTO.pcRegion: PC端刮刮乐区域配置
    - prmtNotPrizeConfigDTO.pcResultPicture: PC抽奖结果图片地址(刮刮乐)
    - prmtNotPrizeConfigDTO.prizeHandType: 奖品派发数量类型(1:不限量；2;限制派发)
    - prmtNotPrizeConfigDTO.prizeName: 奖品名称
    - prmtNotPrizeConfigDTO.prizePicture: 奖品图片
    - prmtNotPrizeConfigDTO.tips: 提示语
    - prmtPrizeConfigList: 奖品配置
    - prmtPrizeConfigList.activityId: 活动id
    - prmtPrizeConfigList.alreadyHandNumber: 已派发数量
    - prmtPrizeConfigList.blindBoxRemark: 盲盒模式奖品文案
    - prmtPrizeConfigList.couponId: 优惠券id
    - prmtPrizeConfigList.limitHandNumber: 奖品限制派发数量
    - prmtPrizeConfigList.mobileRegion: 移动端刮刮乐区域配置
    - prmtPrizeConfigList.mobileResultPicture: 移动端抽奖结果图片地址(刮刮乐)
    - prmtPrizeConfigList.onceBeanAmount: 每份奖品金豆数量
    - prmtPrizeConfigList.pcRegion: PC端刮刮乐区域配置
    - prmtPrizeConfigList.pcResultPicture: PC抽奖结果图片地址(刮刮乐)
    - prmtPrizeConfigList.prizeHandType: 奖品派发数量类型(1:不限量；2;限制派发)
    - prmtPrizeConfigList.prizeId: 奖品id
    - prmtPrizeConfigList.prizeName: 奖品名称
    - prmtPrizeConfigList.prizePicture: 奖品图片
    - prmtPrizeConfigList.prizeType: 奖品类型：1-优惠券，2-赠品兑换码活动 3-金豆
    - prmtPrizeConfigList.sourceId: 奖品来源id：兑换活动id
    - productType: pv抽奖商品配置类型：0-黑名单商品 1-白名单商品
    - remark: 活动说明
    - startTime: 活动开始时间
    - state: 状态(1待审核2待开始3进行中4已结束5已驳回6草稿)
    - winningCounts: 中奖次数
    - winningCountsType: 中奖次数类型(0:不限次数；1:统一次数)
    - wxGuide: 是否开启企微引导：0-否，1-是
    - wxGuidePicture: 企微引导图片地址
    - wxShareAssistPicture: 分享助力小程序分享卡片图
    - wxShareAssistRemark: 分享助力小程序分享卡片文案
    - wxSharePicture: 小程序分享卡片图
    - ydBackgroundPicture: yd活动背景图
    """

    url = "/mgmt/prmt/luckyActivity/addBaseInfo"
    with client.post(url=url, json=data, headers=headers) as r:
        return r

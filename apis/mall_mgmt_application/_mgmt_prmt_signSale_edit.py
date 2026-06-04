import os

from util.client import client

data = {
    "changeAddrLimit": 0,  # 修改活动地址次数限制
    "changeableAddr": False,  # 是否支持修改活动地址：true-支持,false-不支持
    "clause": "",  # 活动条款
    "commitment": "",  # 代购承诺书
    "coverMobile": "",  # 移动端活动封面图
    "coverPc": "",  # PC端活动封面图
    "endTime": "",  # 结束时间
    "id": 0,  # 主键
    "importKey": "",  # 导入操作键
    "introMobile": "",  # 移动端活动介绍
    "introPc": "",  # PC端活动介绍
    "limitCustomer": 0,  # 参与顾客设置:1-所有顾客,2-自定义顾客群,4-自由导入
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
    "minAmount": 0.0,  # 最低支付总金额(百分比)
    "poster": "",  # 活动分享海报
    "promotionCode": "",  # 活动编号
    "promotionName": "",  # 活动名称
    "promotionState": 0,  # 活动状态:1-待审核,2-待开始,3-进行中,4-已结束,5-已驳回,6-草稿
    "remark": "",  # 活动说明
    "renewedGift": False,  # 是否配置续签福利:false-否 true-是
    "renewedGiftList": [{"customPrice": 0.0, "giveMonth": "", "quantity": 0, "serialNo": ""}],  # 续签福利商品集合
    "saleProductDTOList": [{"quantity": 0, "serialNo": "", "stage": 0}],  # 签约购活动产品集合
    "signLimit": 0,  # 活动签约/履约限制具体数值,与signLimitType配合使用
    "signLimitType": 0,  # 活动签约限制类型: -1-不限制, 0-限制每卡可签约数量, 1-限制每卡同时履约次数
    "signedGift": False,  # 是否配置签约赠品:false-否 true-是
    "signedGiftList": [{"customPrice": 0.0, "giveMonth": "", "quantity": 0, "serialNo": ""}],  # 签约赠品集合
    "stages": 0,  # 活动期数
    "startTime": "",  # 开始时间
    "totalAmount": 0.0,  # 签约总金额
    "upgrade": False,  # 是否允许签约购升级 false-否 true-是
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_signSale_edit(data=data, headers=headers):
    """
    编辑签约购活动
    /mgmt/prmt/signSale/edit

    参数说明:
    - changeAddrLimit: 修改活动地址次数限制
    - changeableAddr: 是否支持修改活动地址：true-支持,false-不支持
    - clause: 活动条款
    - commitment: 代购承诺书
    - coverMobile: 移动端活动封面图
    - coverPc: PC端活动封面图
    - endTime: 结束时间
    - id: 主键
    - importKey: 导入操作键
    - introMobile: 移动端活动介绍
    - introPc: PC端活动介绍
    - limitCustomer: 参与顾客设置:1-所有顾客,2-自定义顾客群,4-自由导入
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
    - minAmount: 最低支付总金额(百分比)
    - poster: 活动分享海报
    - promotionCode: 活动编号
    - promotionName: 活动名称
    - promotionState: 活动状态:1-待审核,2-待开始,3-进行中,4-已结束,5-已驳回,6-草稿
    - remark: 活动说明
    - renewedGift: 是否配置续签福利:false-否 true-是
    - renewedGiftList: 续签福利商品集合
    - renewedGiftList.customPrice: 画线价
    - renewedGiftList.giveMonth: 履约月份 或 续签赠送期数,履约月份格式：yyyy-MM,续签赠送期数格式为数值
    - renewedGiftList.quantity: 赠送数量
    - renewedGiftList.serialNo: 赠品产品编码
    - saleProductDTOList: 签约购活动产品集合
    - saleProductDTOList.quantity: 每期购买数量
    - saleProductDTOList.serialNo: 产品编码
    - saleProductDTOList.stage: 活动期数
    - signLimit: 活动签约/履约限制具体数值,与signLimitType配合使用
    - signLimitType: 活动签约限制类型: -1-不限制, 0-限制每卡可签约数量, 1-限制每卡同时履约次数
    - signedGift: 是否配置签约赠品:false-否 true-是
    - signedGiftList: 签约赠品集合
    - signedGiftList.customPrice: 画线价
    - signedGiftList.giveMonth: 履约月份 或 续签赠送期数,履约月份格式：yyyy-MM,续签赠送期数格式为数值
    - signedGiftList.quantity: 赠送数量
    - signedGiftList.serialNo: 赠品产品编码
    - stages: 活动期数
    - startTime: 开始时间
    - totalAmount: 签约总金额
    - upgrade: 是否允许签约购升级 false-否 true-是
    """

    url = "/mgmt/prmt/signSale/edit"
    with client.post(url=url, json=data, headers=headers) as r:
        return r

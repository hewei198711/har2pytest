import os

from util.client import client

data = {
    "businessType": 0,  # 业务类型，1：后台提现；2：失效提现；3：顾客提现
    "cardNo": "",  # 会员卡号
    "couponStatus": 0,  # 使用状态，运营后台使用
    "couponStatusList": [],  # 使用状态集合，商城使用，比如：未使用传[2]；占用中传[3]；已使用传[1]；已失效传[4,5]；已提现传[6,7]
    "currentStoreCode": "",  # 当前登录店铺编号（前端不用传）
    "effectEndTime": "",  # TODO: 添加参数说明
    "effectEndTimeStr": "",  # 发放结束时间-字符串类型
    "effectStartTime": "",  # TODO: 添加参数说明
    "effectStartTimeStr": "",  # 发放开始时间-字符串类型
    "from": 0,  # TODO: 添加参数说明
    "getType": 0,  # 获券类型，1：购物获得；2：月结更新
    "keywordStr": "",  # 关键字字段（店铺后台查询购物礼券使用）
    "leaderCardNo": "",  # 负责人卡号（前端不用传）
    "memberType": 0,  # 顾客类型
    "mobile": "",  # 会员手机号
    "pageNum": 0,  # 页数
    "pageSize": 0,  # 每页显示数
    "platformType": 0,  # 平台类型
    "realname": "",  # 顾客姓名
    "secondCouponIdList": [],  # 秒返券id集合
    "soReturnFlag": False,  # 是否已退货
    "sourceOrderEndMonth": "",  # 来源订单业绩结束月份YYYYMM
    "sourceOrderNo": "",  # 来源订单号
    "sourceOrderStartMonth": "",  # 来源订单业绩开始月份YYYYMM
    "sourceStoreCode": "",  # 服务中心编号
    "withdrawBatch": "",  # 提现批次号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_finance_voucher_getSecondCouponListForShop(data=data, headers=headers):
    """
    购物礼券列表
    /appStore/finance/voucher/getSecondCouponListForShop

    参数说明:
    - businessType: 业务类型，1：后台提现；2：失效提现；3：顾客提现
    - cardNo: 会员卡号
    - couponStatus: 使用状态，运营后台使用
    - couponStatusList: 使用状态集合，商城使用，比如：未使用传[2]；占用中传[3]；已使用传[1]；已失效传[4,5]；已提现传[6,7]
    - currentStoreCode: 当前登录店铺编号（前端不用传）
    - effectEndTimeStr: 发放结束时间-字符串类型
    - effectStartTimeStr: 发放开始时间-字符串类型
    - getType: 获券类型，1：购物获得；2：月结更新
    - keywordStr: 关键字字段（店铺后台查询购物礼券使用）
    - leaderCardNo: 负责人卡号（前端不用传）
    - memberType: 顾客类型
    - mobile: 会员手机号
    - pageNum: 页数
    - pageSize: 每页显示数
    - platformType: 平台类型
    - realname: 顾客姓名
    - secondCouponIdList: 秒返券id集合
    - soReturnFlag: 是否已退货
    - sourceOrderEndMonth: 来源订单业绩结束月份YYYYMM
    - sourceOrderNo: 来源订单号
    - sourceOrderStartMonth: 来源订单业绩开始月份YYYYMM
    - sourceStoreCode: 服务中心编号
    - withdrawBatch: 提现批次号
    """

    url = "/appStore/finance/voucher/getSecondCouponListForShop"
    with client.post(url=url, json=data, headers=headers) as r:
        return r

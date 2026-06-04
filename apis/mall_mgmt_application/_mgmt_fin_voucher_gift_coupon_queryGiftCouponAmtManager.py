import os

from util.client import client

data = {
    "applyTimeEnd": "",  # 使用时间结束
    "applyTimeStart": "",  # 使用时间开始
    "businessType": 0,  # 业务类型 1:提现   2:到期转出
    "cardNo": "",  # 会员卡号
    "claimTimeEnd": "",  # 发放月份结束
    "claimTimeStart": "",  # 发放月份开始
    "couponTimeEnd": "",  # 礼券月份结束
    "couponTimeStart": "",  # 礼券月份开始
    "currentStoreCode": "",  # 当前登录店铺编号（前端不用传）
    "expiresTimeEnd": "",  # 到期月份结束
    "expiresTimeStart": "",  # 到期月份开始
    "freightCouponStatus": 0,  # 电子礼券状态 1:已使用   2:未使用   3:占用中   4:冻结中  5:已转出 6:已失效
    "from": 0,  # TODO: 添加参数说明
    "keywordStr": "",  # 关键字字段（店铺后台查询电子礼券使用）
    "leaderCardNo": "",  # 负责人卡号（前端不用传）
    "mobile": "",  # 手机号码
    "orderNo": "",  # 订单编号
    "pageNum": 0,  # 页数
    "pageSize": 0,  # 每页显示数
    "realname": "",  # 姓名
    "shopCode": "",  # 服务中心编码
    "syncBatchNo": "",  # 推送批次
    "updateTimeEnd": "",  # 操作时间结束
    "updateTimeStart": "",  # 操作时间开始
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_fin_voucher_gift_coupon_queryGiftCouponAmtManager(data=data, headers=headers):
    """
    电子礼券金额统计(商城后台)
    /mgmt/fin/voucher/gift/coupon/queryGiftCouponAmtManager

    参数说明:
    - applyTimeEnd: 使用时间结束
    - applyTimeStart: 使用时间开始
    - businessType: 业务类型 1:提现   2:到期转出
    - cardNo: 会员卡号
    - claimTimeEnd: 发放月份结束
    - claimTimeStart: 发放月份开始
    - couponTimeEnd: 礼券月份结束
    - couponTimeStart: 礼券月份开始
    - currentStoreCode: 当前登录店铺编号（前端不用传）
    - expiresTimeEnd: 到期月份结束
    - expiresTimeStart: 到期月份开始
    - freightCouponStatus: 电子礼券状态 1:已使用   2:未使用   3:占用中   4:冻结中  5:已转出 6:已失效
    - keywordStr: 关键字字段（店铺后台查询电子礼券使用）
    - leaderCardNo: 负责人卡号（前端不用传）
    - mobile: 手机号码
    - orderNo: 订单编号
    - pageNum: 页数
    - pageSize: 每页显示数
    - realname: 姓名
    - shopCode: 服务中心编码
    - syncBatchNo: 推送批次
    - updateTimeEnd: 操作时间结束
    - updateTimeStart: 操作时间开始
    """

    url = "/mgmt/fin/voucher/gift/coupon/queryGiftCouponAmtManager"
    with client.post(url=url, json=data, headers=headers) as r:
        return r

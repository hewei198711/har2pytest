import os

from util.client import client

data = {
    "cardNo": "",  # 会员卡号
    "from": 0,  # TODO: 添加参数说明
    "memberType": 0,  # 顾客类型
    "mobile": "",  # 会员手机号
    "pageNum": 0,  # 页数
    "pageSize": 0,  # 每页显示数
    "withdrawEndTime": "",  # TODO: 添加参数说明
    "withdrawEndTimeStr": "",  # 提现结束时间yyyy-MM-dd，提供给WEB使用
    "withdrawStartTime": "",  # TODO: 添加参数说明
    "withdrawStartTimeStr": "",  # 提现开始时间yyyy-MM-dd，提供给WEB使用
    "withdrawStatus": 0,  # 提现状态，1：待受理；2：已受理；3：已撤销
    "withdrawTimeStr": "",  # 提现时间yyyy-MM，提供给APP和小程序使用
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_fin_voucher_gift_coupon_queryPendingWithdrawList(data=data, headers=headers):
    """
    电子礼券提现列表（待受理不分页）
    /mgmt/fin/voucher/gift/coupon/queryPendingWithdrawList

    参数说明:
    - cardNo: 会员卡号
    - memberType: 顾客类型
    - mobile: 会员手机号
    - pageNum: 页数
    - pageSize: 每页显示数
    - withdrawEndTimeStr: 提现结束时间yyyy-MM-dd，提供给WEB使用
    - withdrawStartTimeStr: 提现开始时间yyyy-MM-dd，提供给WEB使用
    - withdrawStatus: 提现状态，1：待受理；2：已受理；3：已撤销
    - withdrawTimeStr: 提现时间yyyy-MM，提供给APP和小程序使用
    """

    url = "/mgmt/fin/voucher/gift/coupon/queryPendingWithdrawList"
    with client.post(url=url, json=data, headers=headers) as r:
        return r

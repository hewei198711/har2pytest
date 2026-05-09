import os

from util.client import client

data = {
    "endDate": "",  # 结束日期(yyyy-MM-dd)
    "orderRepaymentTime": "",  # 汇款时间排序的字段
    "pageNum": 0,  # 当前页,默认第1页
    "pageSize": 0,  # 每页显示数,默认10条
    "startDate": "",  # 开始日期(yyyy-MM-dd)
    "storeCode": "",  # 当前用户的StoreCode
    "type": 0,  # 顾客类型:0全部,1押货款,2退款,3订货款,4开店保证金,5超额保证金,6 1:3押货款退款申请，7超额保证金退款申请，8超额押货款， 9超额押货款退款，10手工确认押货款，11转销售，12退结点余款， 13押货款还钱包欠款，14还欠款
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_mortgageAmount_history_invtHistoryRepaymentLog(data=data, headers=headers):
    """
    汇款明细
    /appStore/mortgageAmount/history/invtHistoryRepaymentLog

    参数说明:
    - endDate: 结束日期(yyyy-MM-dd)
    - orderRepaymentTime: 汇款时间排序的字段
    - pageNum: 当前页,默认第1页
    - pageSize: 每页显示数,默认10条
    - startDate: 开始日期(yyyy-MM-dd)
    - storeCode: 当前用户的StoreCode
    - type: 顾客类型:0全部,1押货款,2退款,3订货款,4开店保证金,5超额保证金,6 1:3押货款退款申请，7超额保证金退款申请，8超额押货款， 9超额押货款退款，10手工确认押货款，11转销售，12退结点余款， 13押货款还钱包欠款，14还欠款
    """

    url = "/appStore/mortgageAmount/history/invtHistoryRepaymentLog"
    with client.post(url=url, json=data, headers=headers) as r:
        return r

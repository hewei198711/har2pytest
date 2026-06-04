import os

from util.client import client

data = {
    "cardNo": "",  # 会员卡号
    "channelCode": 0,  # 支付渠道
    "companyNo": "",  # 分公司编号
    "from": 0,  # TODO: 添加参数说明
    "memberId": "",  # 顾客编号
    "pageNum": 0,  # 页数
    "pageSize": 0,  # 每页显示数
    "status": 0,  # 平账状态
    "tradeDate": "",  # 交易日期
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_pay_verifyAcct_query(data=data, headers=headers):
    """
    查询支付渠道对账结果信息
    /mgmt/pay/verifyAcct/query

    参数说明:
    - cardNo: 会员卡号
    - channelCode: 支付渠道
    - companyNo: 分公司编号
    - memberId: 顾客编号
    - pageNum: 页数
    - pageSize: 每页显示数
    - status: 平账状态
    - tradeDate: 交易日期
    """

    url = "/mgmt/pay/verifyAcct/query"
    with client.post(url=url, json=data, headers=headers) as r:
        return r

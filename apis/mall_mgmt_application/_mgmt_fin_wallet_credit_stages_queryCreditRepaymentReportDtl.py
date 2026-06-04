import os

from util.client import client

data = {
    "from": 0,  # TODO: 添加参数说明
    "pageNum": 0,  # 页数
    "pageSize": 0,  # 每页显示数
    "walletId": 0,  # 钱包id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_fin_wallet_credit_stages_queryCreditRepaymentReportDtl(data=data, headers=headers):
    """
    信用额还款情况报表详情
    /mgmt/fin/wallet/credit/stages/queryCreditRepaymentReportDtl

    参数说明:
    - pageNum: 页数
    - pageSize: 每页显示数
    - walletId: 钱包id
    """

    url = "/mgmt/fin/wallet/credit/stages/queryCreditRepaymentReportDtl"
    with client.post(url=url, json=data, headers=headers) as r:
        return r

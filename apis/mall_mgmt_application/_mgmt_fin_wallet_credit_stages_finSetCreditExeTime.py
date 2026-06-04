import os

from util.client import client

data = {
    "creditExeTime": "",  # 设置执行时间 格式为：yyyy-MM
    "creditStagesCode": "",  # 信用额分期管理编码
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_fin_wallet_credit_stages_finSetCreditExeTime(data=data, headers=headers):
    """
    设置执行时间
    /mgmt/fin/wallet/credit/stages/finSetCreditExeTime

    参数说明:
    - creditExeTime: 设置执行时间 格式为：yyyy-MM
    - creditStagesCode: 信用额分期管理编码
    """

    url = "/mgmt/fin/wallet/credit/stages/finSetCreditExeTime"
    with client.post(url=url, json=data, headers=headers) as r:
        return r

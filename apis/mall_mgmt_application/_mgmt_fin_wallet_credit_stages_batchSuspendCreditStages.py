import os

from util.client import client

data = {
    "creditDeductedFlag": 0,  # 是否当月暂不扣除 1：是,0：否
    "creditStagesCodeList": [],  # TODO: 添加参数说明
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_fin_wallet_credit_stages_batchSuspendCreditStages(data=data, headers=headers):
    """
    批量暂停
    /mgmt/fin/wallet/credit/stages/batchSuspendCreditStages

    参数说明:
    - creditDeductedFlag: 是否当月暂不扣除 1：是,0：否
    """

    url = "/mgmt/fin/wallet/credit/stages/batchSuspendCreditStages"
    with client.post(url=url, json=data, headers=headers) as r:
        return r

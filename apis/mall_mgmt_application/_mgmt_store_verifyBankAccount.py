import os

from util.client import client

data = {
    "id": 0,  # TODO: 添加参数说明
    "opType": 0,  # 操作类型 1新增 2修改 3作废
    "verifyRemark": "",  # 审核备注
    "verifyStatus": 0,  # 审核状态 1审核通过 2审核不通过 3待审核
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_verifyBankAccount(data=data, headers=headers):
    """
    审批银行账号
    /mgmt/store/verifyBankAccount

    参数说明:
    - opType: 操作类型 1新增 2修改 3作废
    - verifyRemark: 审核备注
    - verifyStatus: 审核状态 1审核通过 2审核不通过 3待审核
    """

    url = "/mgmt/store/verifyBankAccount"
    with client.post(url=url, json=data, headers=headers) as r:
        return r

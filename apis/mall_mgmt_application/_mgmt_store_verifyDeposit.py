import os

from util.client import client

data = {
    "ids": "",  # 列表数据主键id，多个用逗号分隔
    "verifyRemark": "",  # 审核备注
    "verifyStatus": 0,  # 审核状态 1通过 2不通过
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_verifyDeposit(data=data, headers=headers):
    """
    批量审批保证金
    /mgmt/store/verifyDeposit

    参数说明:
    - ids: 列表数据主键id，多个用逗号分隔
    - verifyRemark: 审核备注
    - verifyStatus: 审核状态 1通过 2不通过
    """

    url = "/mgmt/store/verifyDeposit"
    with client.post(url=url, json=data, headers=headers) as r:
        return r

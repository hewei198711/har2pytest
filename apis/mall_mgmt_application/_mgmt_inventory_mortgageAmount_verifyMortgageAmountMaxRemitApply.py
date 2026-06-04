import os

from util.client import client

data = {
    "ids": [],  # 审核主键id
    "verifyRemark": "",  # 审核备注
    "verifyStatus": 0,  # 审核状态 1通过 2不通过
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_mortgageAmount_verifyMortgageAmountMaxRemitApply(data=data, headers=headers):
    """
    押货额度变更审核
    /mgmt/inventory/mortgageAmount/verifyMortgageAmountMaxRemitApply

    参数说明:
    - ids: 审核主键id
    - verifyRemark: 审核备注
    - verifyStatus: 审核状态 1通过 2不通过
    """

    url = "/mgmt/inventory/mortgageAmount/verifyMortgageAmountMaxRemitApply"
    with client.post(url=url, json=data, headers=headers) as r:
        return r

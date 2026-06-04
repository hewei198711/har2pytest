import os

from util.client import client

data = {
    "ids": [],  # 审核记录主键ids
    "verifier": "",  # 审核人
    "verifyRemark": "",  # 审核备注
    "verifyStatus": 0,  # 审核状态 1通过 2不通过
    "verifyTime": "",  # 审核时间
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_discredit_verify(data=data, headers=headers):
    """
    信誉额审核/批量审核
    /mgmt/inventory/discredit/verify

    参数说明:
    - ids: 审核记录主键ids
    - verifier: 审核人
    - verifyRemark: 审核备注
    - verifyStatus: 审核状态 1通过 2不通过
    - verifyTime: 审核时间
    """

    url = "/mgmt/inventory/discredit/verify"
    with client.post(url=url, json=data, headers=headers) as r:
        return r

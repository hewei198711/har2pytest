import os

from util.client import client

data = {
    "ids": [],  # 主键id
    "verifyRemark": "",  # 审核备注
    "verifyResult": 0,  # 1->通过  2-> 拒绝
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_disManualInputRemit_batchVerify(data=data, headers=headers):
    """
    85折手工录入流水批量审核
    /mgmt/inventory/disManualInputRemit/batchVerify

    参数说明:
    - ids: 主键id
    - verifyRemark: 审核备注
    - verifyResult: 1->通过  2-> 拒绝
    """

    url = "/mgmt/inventory/disManualInputRemit/batchVerify"
    with client.post(url=url, json=data, headers=headers) as r:
        return r

import os

from util.client import client

data = {
    "ids": [],  # 主键id
    "remark": "",  # 审核备注
    "verifyStatus": 0,  # 审核结果 1审核通过 2审核不通过
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_return_config_deal(data=data, headers=headers):
    """
    审核/批量审核
    /mgmt/inventory/return/config/deal

    参数说明:
    - ids: 主键id
    - remark: 审核备注
    - verifyStatus: 审核结果 1审核通过 2审核不通过
    """

    url = "/mgmt/inventory/return/config/deal"
    with client.post(url=url, json=data, headers=headers) as r:
        return r

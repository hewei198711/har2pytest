import os

from util.client import client

data = {
    "id": 0,  # 主键id
    "remark": "",  # 备注
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_editContractRemark(data=data, headers=headers):
    """
    编辑合同备注
    /mgmt/store/editContractRemark

    参数说明:
    - id: 主键id
    - remark: 备注
    """

    url = "/mgmt/store/editContractRemark"
    with client.post(url=url, json=data, headers=headers) as r:
        return r

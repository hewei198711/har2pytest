import os

from util.client import client

data = {
    "contractManageId": "",  # 合同管理ID
    "remark": "",  # 备注
    "storeCode": "",  # 服务中心编号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_undoContract(data=data, headers=headers):
    """
    撤销合同
    /mgmt/store/undoContract

    参数说明:
    - contractManageId: 合同管理ID
    - remark: 备注
    - storeCode: 服务中心编号
    """

    url = "/mgmt/store/undoContract"
    with client.post(url=url, json=data, headers=headers) as r:
        return r

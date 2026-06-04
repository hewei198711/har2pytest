import os

from util.client import client

data = {
    "id": 0,  # 变更ID
    "storeCode": "",  # 服务中心编码
    "verifyRemark": "",  # 审核备注
    "verifyStatus": 0,  # 审核状态 1通过 2不通过
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_verifyProfileChange(data=data, headers=headers):
    """
    审核服务中心资料变更
    /mgmt/store/verifyProfileChange

    参数说明:
    - id: 变更ID
    - storeCode: 服务中心编码
    - verifyRemark: 审核备注
    - verifyStatus: 审核状态 1通过 2不通过
    """

    url = "/mgmt/store/verifyProfileChange"
    with client.post(url=url, json=data, headers=headers) as r:
        return r

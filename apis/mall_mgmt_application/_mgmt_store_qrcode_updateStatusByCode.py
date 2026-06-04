import os

from util.client import client

data = {
    "remark": "",  # 备注
    "status": 0,  # 活码状态，0-禁用，1-启用
    "storeCode": "",  # 服务中心编号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_qrcode_updateStatusByCode(data=data, headers=headers):
    """
    根据服务中心编号修改活码状态
    /mgmt/store/qrcode/updateStatusByCode

    参数说明:
    - remark: 备注
    - status: 活码状态，0-禁用，1-启用
    - storeCode: 服务中心编号
    """

    url = "/mgmt/store/qrcode/updateStatusByCode"
    with client.post(url=url, json=data, headers=headers) as r:
        return r

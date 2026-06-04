import os

from util.client import client

params = {
    "certificatesNo": "",  # certificatesNo
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_checkStoreCertificatesNoIsExist(params=params, headers=headers):
    """
    校验证件号唯一性，true为存在相同值
    /mgmt/store/checkStoreCertificatesNoIsExist

    参数说明:
    - certificatesNo: certificatesNo
    """

    url = "/mgmt/store/checkStoreCertificatesNoIsExist"
    with client.get(url=url, params=params, headers=headers) as r:
        return r

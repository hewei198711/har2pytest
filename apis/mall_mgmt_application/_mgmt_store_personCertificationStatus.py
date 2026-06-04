import os

from util.client import client

params = {
    "account": "",  # oa工号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_personCertificationStatus(params=params, headers=headers):
    """
    oa人员实名认证状态查询
    /mgmt/store/personCertificationStatus

    参数说明:
    - account: oa工号
    """

    url = "/mgmt/store/personCertificationStatus"
    with client.get(url=url, params=params, headers=headers) as r:
        return r

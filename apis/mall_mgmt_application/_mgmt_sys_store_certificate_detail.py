import os

from util.client import client

params = {
    "id": 0,  # id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_sys_store_certificate_detail(params=params, headers=headers):
    """
    查看详情
    /mgmt/sys/store/certificate/detail

    参数说明:
    - id: id
    """

    url = "/mgmt/sys/store/certificate/detail"
    with client.get(url=url, params=params, headers=headers) as r:
        return r

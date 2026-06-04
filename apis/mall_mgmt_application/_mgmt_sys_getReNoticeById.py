import os

from util.client import client

params = {
    "id": 0,  # id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_sys_getReNoticeById(params=params, headers=headers):
    """
    查询退货须知详情
    /mgmt/sys/getReNoticeById

    参数说明:
    - id: id
    """

    url = "/mgmt/sys/getReNoticeById"
    with client.get(url=url, params=params, headers=headers) as r:
        return r

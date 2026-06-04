import os

from util.client import client

params = {
    "id": 0,  # id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_sys_delMobiNoDelyConf(params=params, headers=headers):
    """
    指定手机号不发货配置-删除收件人手机号
    /mgmt/sys/delMobiNoDelyConf

    参数说明:
    - id: id
    """

    url = "/mgmt/sys/delMobiNoDelyConf"
    with client.get(url=url, params=params, headers=headers) as r:
        return r

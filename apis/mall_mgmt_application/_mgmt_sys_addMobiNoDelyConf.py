import os

from util.client import client

params = {
    "mobile": "",  # mobile
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_sys_addMobiNoDelyConf(params=params, headers=headers):
    """
    指定手机号不发货配置-添加收件人手机号
    /mgmt/sys/addMobiNoDelyConf

    参数说明:
    - mobile: mobile
    """

    url = "/mgmt/sys/addMobiNoDelyConf"
    with client.get(url=url, params=params, headers=headers) as r:
        return r

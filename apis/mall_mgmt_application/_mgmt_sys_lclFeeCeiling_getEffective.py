import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_sys_lclFeeCeiling_getEffective(headers=headers):
    """
    获取生效中的拼箱费上限
    /mgmt/sys/lclFeeCeiling/getEffective
    """

    url = "/mgmt/sys/lclFeeCeiling/getEffective"
    with client.get(url=url, headers=headers) as r:
        return r

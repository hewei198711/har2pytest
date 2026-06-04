import os

from util.client import client

params = {
    "keyword": "",  # keyword
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_share_selectMember(params=params, headers=headers):
    """
    手机号或卡号查询顾客
    /mgmt/prmt/share/selectMember

    参数说明:
    - keyword: keyword
    """

    url = "/mgmt/prmt/share/selectMember"
    with client.get(url=url, params=params, headers=headers) as r:
        return r

import os

from util.client import client

params = {
    "uCongNo": "",  # uCongNo
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_checkUCongNoIsExist(params=params, headers=headers):
    """
    检查油葱编号是否存在，true为存在相同值
    /mgmt/store/checkUCongNoIsExist

    参数说明:
    - uCongNo: uCongNo
    """

    url = "/mgmt/store/checkUCongNoIsExist"
    with client.get(url=url, params=params, headers=headers) as r:
        return r

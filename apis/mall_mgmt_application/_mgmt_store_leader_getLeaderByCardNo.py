import os

from util.client import client

params = {
    "cardNo": "",  # 会员卡号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_leader_getLeaderByCardNo(params=params, headers=headers):
    """
    根据会员卡号获取服务中心负责人信息
    /mgmt/store/leader/getLeaderByCardNo

    参数说明:
    - cardNo: 会员卡号
    """

    url = "/mgmt/store/leader/getLeaderByCardNo"
    with client.get(url=url, params=params, headers=headers) as r:
        return r

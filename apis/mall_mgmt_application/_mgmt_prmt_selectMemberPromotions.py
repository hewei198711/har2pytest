import os

from util.client import client

params = {
    "cardNo": "",  # cardNo
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_selectMemberPromotions(params=params, headers=headers):
    """
    查询顾客可参加的活动
    /mgmt/prmt/selectMemberPromotions

    参数说明:
    - cardNo: cardNo
    """

    url = "/mgmt/prmt/selectMemberPromotions"
    with client.get(url=url, params=params, headers=headers) as r:
        return r

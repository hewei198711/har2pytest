import os

from util.client import client

params = {
    "applyId": 0,  # 申请id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_store_dis_mortgage_modifyApply_detail(params=params, headers=headers):
    """
    详情修改申请
    /appStore/store/dis/mortgage/modifyApply/detail

    参数说明:
    - applyId: 申请id
    """

    url = "/appStore/store/dis/mortgage/modifyApply/detail"
    with client.get(url=url, params=params, headers=headers) as r:
        return r

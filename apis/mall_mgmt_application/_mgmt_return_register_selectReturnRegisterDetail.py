import os

from util.client import client

params = {
    "id": 0,  # id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_return_register_selectReturnRegisterDetail(params=params, headers=headers):
    """
    查询登记退货信息详情
    /mgmt/return/register/selectReturnRegisterDetail

    参数说明:
    - id: id
    """

    url = "/mgmt/return/register/selectReturnRegisterDetail"
    with client.get(url=url, params=params, headers=headers) as r:
        return r

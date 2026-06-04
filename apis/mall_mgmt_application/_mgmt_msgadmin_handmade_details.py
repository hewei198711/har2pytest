import os

from util.client import client

params = {
    "planCode": "",  # planCode
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_msgadmin_handmade_details(params=params, headers=headers):
    """
    详情
    /mgmt/msgadmin/handmade/details

    参数说明:
    - planCode: planCode
    """

    url = "/mgmt/msgadmin/handmade/details"
    with client.get(url=url, params=params, headers=headers) as r:
        return r

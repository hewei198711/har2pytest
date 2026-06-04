import os

from util.client import client

params = {
    "date": "",  # date
    "type": 0,  # type
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_dataAdmin_goldBean_comparison(params=params, headers=headers):
    """
    金豆百分比
    /mgmt/dataAdmin/goldBean/comparison

    参数说明:
    - date: date
    - type: type
    """

    url = "/mgmt/dataAdmin/goldBean/comparison"
    with client.get(url=url, params=params, headers=headers) as r:
        return r

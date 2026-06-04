import os

from util.client import client

data = {
    "id": 0,  # 法规咨询id
    "sort": 0,  # 排序
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_sys_informationLaw_sort(data=data, headers=headers):
    """
    法规咨询(新)-排序
    /mgmt/sys/informationLaw/sort

    参数说明:
    - id: 法规咨询id
    - sort: 排序
    """

    url = "/mgmt/sys/informationLaw/sort"
    with client.post(url=url, json=data, headers=headers) as r:
        return r

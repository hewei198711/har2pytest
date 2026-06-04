import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
}


def _mgmt_acc_instructions_sort(headers=headers):
    """
    使用说明排序
    /mgmt/acc/instructions/sort
    """

    url = "/mgmt/acc/instructions/sort"
    with client.post(url=url, headers=headers) as r:
        return r

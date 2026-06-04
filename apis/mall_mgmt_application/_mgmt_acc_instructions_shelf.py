import os

from util.client import client

data = {
    "id": "",  # TODO: 添加参数说明
    "shelfStatus": 0,  # 上架状态,0：待上架; 1：已上架；2：已下架
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
}


def _mgmt_acc_instructions_shelf(data=data, headers=headers):
    """
    使用说明上下架
    /mgmt/acc/instructions/shelf

    参数说明:
    - shelfStatus: 上架状态,0：待上架; 1：已上架；2：已下架
    """

    url = "/mgmt/acc/instructions/shelf"
    with client.post(url=url, json=data, headers=headers) as r:
        return r

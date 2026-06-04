import os

from util.client import client

data = {
    "id": 0,  # id
    "notice": "",  # 退货须知内容
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_sys_updateReNoticeById(data=data, headers=headers):
    """
    修改退货须知详情
    /mgmt/sys/updateReNoticeById

    参数说明:
    - id: id
    - notice: 退货须知内容
    """

    url = "/mgmt/sys/updateReNoticeById"
    with client.post(url=url, json=data, headers=headers) as r:
        return r

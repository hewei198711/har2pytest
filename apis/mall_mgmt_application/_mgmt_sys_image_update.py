import os

from util.client import client

data = {
    "channel": 0,  # 使用对象： 1->服务中心; 2 ->商城;3->服务中心+商城
    "id": 0,  # 主键id
    "manualName": "",  # 手册名称
    "manualUrl": "",  # 手册地址
    "status": 0,  # 状态：0.禁用，1.启用
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_sys_image_update(data=data, headers=headers):
    """
    修改形象手册信息
    /mgmt/sys/image/update

    参数说明:
    - channel: 使用对象： 1->服务中心; 2 ->商城;3->服务中心+商城
    - id: 主键id
    - manualName: 手册名称
    - manualUrl: 手册地址
    - status: 状态：0.禁用，1.启用
    """

    url = "/mgmt/sys/image/update"
    with client.post(url=url, json=data, headers=headers) as r:
        return r

import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_msgadmin_scene_init(headers=headers):
    """
    系统消息管理-场景初始化查询接口
    /mgmt/msgadmin/scene/init
    """

    url = "/mgmt/msgadmin/scene/init"
    with client.get(url=url, headers=headers) as r:
        return r

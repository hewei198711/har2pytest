import os

from util.client import client

data = {
    "field": "",  # 字段
    "fieldDesc": "",  # 描述
    "id": 0,  # 自增主键
    "level": 0,  #  1 系统消息; 2 手工消息
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_msgadmin_param_insertOrUpdate(data=data, headers=headers):
    """
    insertOrUpdate
    /mgmt/msgadmin/param/insertOrUpdate

    参数说明:
    - field: 字段
    - fieldDesc: 描述
    - id: 自增主键
    - level:  1 系统消息; 2 手工消息
    """

    url = "/mgmt/msgadmin/param/insertOrUpdate"
    with client.post(url=url, json=data, headers=headers) as r:
        return r

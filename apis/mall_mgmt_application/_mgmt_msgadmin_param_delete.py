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


def _mgmt_msgadmin_param_delete(data=data, headers=headers):
    """
    删除模版参数
    /mgmt/msgadmin/param/delete

    参数说明:
    - field: 字段
    - fieldDesc: 描述
    - id: 自增主键
    - level:  1 系统消息; 2 手工消息
    """

    url = "/mgmt/msgadmin/param/delete"
    with client.post(url=url, json=data, headers=headers) as r:
        return r

import os

from util.client import client

data = {
    "id": 0,  # 主键id
    "typeName": "",  # 表格名称
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_sys_table_type_save(data=data, headers=headers):
    """
    保存表格类型信息
    /mgmt/sys/table/type/save

    参数说明:
    - id: 主键id
    - typeName: 表格名称
    """

    url = "/mgmt/sys/table/type/save"
    with client.post(url=url, json=data, headers=headers) as r:
        return r

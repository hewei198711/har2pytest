import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_sys_table_type_list(headers=headers):
    """
    查询表格类型集合
    /mgmt/sys/table/type/list
    """

    url = "/mgmt/sys/table/type/list"
    with client.get(url=url, headers=headers) as r:
        return r

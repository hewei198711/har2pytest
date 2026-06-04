import os

from util.client import client

params = {
    "id": 0,  # id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
    "content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}


def _mgmt_store_permissionPackage_del_id(params=params, headers=headers):
    """
    删除权限包
    /mgmt/store/permissionPackage/del/{id}

    参数说明:
    - id: id
    """

    url = f"/mgmt/store/permissionPackage/del/{params['id']}"
    with client.get(url=url, headers=headers) as r:
        return r

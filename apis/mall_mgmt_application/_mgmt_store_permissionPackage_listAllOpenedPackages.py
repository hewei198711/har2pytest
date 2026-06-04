import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_permissionPackage_listAllOpenedPackages(headers=headers):
    """
    列出所有开启状态的权限包
    /mgmt/store/permissionPackage/listAllOpenedPackages
    """

    url = "/mgmt/store/permissionPackage/listAllOpenedPackages"
    with client.get(url=url, headers=headers) as r:
        return r

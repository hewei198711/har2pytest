import os

from util.client import client

params = {
    "storeCode": "",  # storeCode
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_common_isStoreCompanyHasHomeTakePermission(params=params, headers=headers):
    """
    查看服务中心所属分公司是否开通了上门取件功能
    /mgmt/inventory/common/isStoreCompanyHasHomeTakePermission

    参数说明:
    - storeCode: storeCode
    """

    url = "/mgmt/inventory/common/isStoreCompanyHasHomeTakePermission"
    with client.get(url=url, params=params, headers=headers) as r:
        return r

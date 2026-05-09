import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
}


def _appStore_common_isStoreCompanyHasHomeTakePermission(headers=headers):
    """
    查看服务中心所属分公司是否开通了上门取件功能
    /appStore/common/isStoreCompanyHasHomeTakePermission
    """

    url = "/appStore/common/isStoreCompanyHasHomeTakePermission"
    with client.get(url=url, headers=headers) as r:
        return r

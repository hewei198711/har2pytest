import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_store_inventory_mortgageAmount_isCanApplyCreditOrMaxRemit(headers=headers):
    """
    查询前台是否能发起申请押货额/信誉额申请
    /appStore/store/inventory/mortgageAmount/isCanApplyCreditOrMaxRemit
    """

    url = "/appStore/store/inventory/mortgageAmount/isCanApplyCreditOrMaxRemit"
    with client.get(url=url, headers=headers) as r:
        return r

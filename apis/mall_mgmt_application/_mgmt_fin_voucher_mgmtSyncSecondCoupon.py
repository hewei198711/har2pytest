import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
    "content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}


def _mgmt_fin_voucher_mgmtSyncSecondCoupon(headers=headers):
    """
    购物礼券派发管理同步并更新
    /mgmt/fin/voucher/mgmtSyncSecondCoupon
    """

    url = "/mgmt/fin/voucher/mgmtSyncSecondCoupon"
    with client.post(url=url, headers=headers) as r:
        return r

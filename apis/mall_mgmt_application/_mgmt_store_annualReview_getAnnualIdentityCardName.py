import os

from util.client import client

params = {
    "storeCode": "",  # storeCode
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_annualReview_getAnnualIdentityCardName(params=params, headers=headers):
    """
    获取身份证年审姓名信息
    /mgmt/store/annualReview/getAnnualIdentityCardName

    参数说明:
    - storeCode: storeCode
    """

    url = "/mgmt/store/annualReview/getAnnualIdentityCardName"
    with client.get(url=url, params=params, headers=headers) as r:
        return r

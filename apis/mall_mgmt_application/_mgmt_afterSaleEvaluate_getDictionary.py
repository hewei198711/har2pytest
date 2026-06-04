import os

from util.client import client

params = {
    "dicType": "",  # dicType
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
}


def _mgmt_afterSaleEvaluate_getDictionary(params=params, headers=headers):
    """
    查询-自动评价天数设置
    /mgmt/afterSaleEvaluate/getDictionary

    参数说明:
    - dicType: dicType
    """

    url = "/mgmt/afterSaleEvaluate/getDictionary"
    with client.get(url=url, params=params, headers=headers) as r:
        return r

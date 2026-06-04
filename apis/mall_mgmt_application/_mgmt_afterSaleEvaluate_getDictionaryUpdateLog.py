import os

from util.client import client

params = {
    "dicType": "",  # dicType
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
}


def _mgmt_afterSaleEvaluate_getDictionaryUpdateLog(params=params, headers=headers):
    """
    查询-自动评价天数设置-操作记录
    /mgmt/afterSaleEvaluate/getDictionaryUpdateLog

    参数说明:
    - dicType: dicType
    """

    url = "/mgmt/afterSaleEvaluate/getDictionaryUpdateLog"
    with client.get(url=url, params=params, headers=headers) as r:
        return r

import os

from util.client import client

params = {
    "exchangeType": "",  # 换购类型1产品换购2PV达标换购3数量达标换购4金额达标换购
    "key": "",  # key
    "promotionType": "",  # 活动类型1活动2换购
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_getImportErrorList(params=params, headers=headers):
    """
    下载导入错误商品列表
    /mgmt/prmt/getImportErrorList

    参数说明:
    - exchangeType: 换购类型1产品换购2PV达标换购3数量达标换购4金额达标换购
    - key: key
    - promotionType: 活动类型1活动2换购
    """

    url = "/mgmt/prmt/getImportErrorList"
    with client.get(url=url, params=params, headers=headers) as r:
        return r

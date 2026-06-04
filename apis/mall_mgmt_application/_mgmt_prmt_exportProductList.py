import os

from util.client import client

params = {
    "exchangeType": "",  # 换购类型1产品换购2PV达标换购3数量达标换购4金额达标换购
    "product": "",  # 商品编码或名称
    "promotionId": "",  # 活动或换购id
    "promotionType": "",  # 活动类型1活动2换购4预售
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_exportProductList(params=params, headers=headers):
    """
    活动产品导出（详情）
    /mgmt/prmt/exportProductList

    参数说明:
    - exchangeType: 换购类型1产品换购2PV达标换购3数量达标换购4金额达标换购
    - product: 商品编码或名称
    - promotionId: 活动或换购id
    - promotionType: 活动类型1活动2换购4预售
    """

    url = "/mgmt/prmt/exportProductList"
    with client.get(url=url, params=params, headers=headers) as r:
        return r

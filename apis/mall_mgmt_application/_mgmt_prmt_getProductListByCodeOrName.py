import os

from util.client import client

params = {
    "id": "",  # 活动id
    "productCode": "",  # 产品编码
    "productName": "",  # productName
    "type": "",  # 搜索来源:1活动 2换购 3加购 4预售 null优惠券
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_getProductListByCodeOrName(params=params, headers=headers):
    """
    根据产品编码或名称搜索产品（新建活动）
    /mgmt/prmt/getProductListByCodeOrName

    参数说明:
    - id: 活动id
    - productCode: 产品编码
    - productName: productName
    - type: 搜索来源:1活动 2换购 3加购 4预售 null优惠券
    """

    url = "/mgmt/prmt/getProductListByCodeOrName"
    with client.get(url=url, params=params, headers=headers) as r:
        return r

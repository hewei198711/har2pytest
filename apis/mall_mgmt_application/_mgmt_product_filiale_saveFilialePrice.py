import os

from util.client import client

data = {
    "beijingCompanyPrice": "",  # 北京分公司价格
    "otherCompanyPrice": "",  # 除北京外分公司价格
    "priceCatalogId": 0,  # 所属类别id
    "productId": 0,  # 商品id
    "secondCompanyPrice": "",  # 二级分公司价格
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_product_filiale_saveFilialePrice(data=data, headers=headers):
    """
    分公司价格信息添加修改
    /mgmt/product/filiale/saveFilialePrice

    参数说明:
    - beijingCompanyPrice: 北京分公司价格
    - otherCompanyPrice: 除北京外分公司价格
    - priceCatalogId: 所属类别id
    - productId: 商品id
    - secondCompanyPrice: 二级分公司价格
    """

    url = "/mgmt/product/filiale/saveFilialePrice"
    with client.post(url=url, json=data, headers=headers) as r:
        return r

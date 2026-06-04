import os

from util.client import client

params = {
    "beginDate": 0,  # 开始时间
    "endDate": 0,  # 结束时间
    "maxRetailPrice": 0.0,  # 零售价结束
    "minRetailPrice": 0.0,  # 零售价开始
    "pageNum": 0,  # 页码
    "pageSize": 0,  # 页面大小
    "priceCatalogId": 0,  # 所属类别id
    "productStatus": 0,  # 商品状态 6-待生效 7-已上架 8-已下架
    "propertyRights": "",  # 产权
    "saleCompanyId": 0,  # 销售主体id
    "serialNo": "",  # 商品编码
    "status": 0,  # 0-待审核 1-已通过 2-未通过 3-已撤回 4-待添加 5-全部
    "title": "",  # 商品名称
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_product_filiale_export(params=params, headers=headers):
    """
    导出--文件流
    /mgmt/product/filiale/export

    参数说明:
    - beginDate: 开始时间
    - endDate: 结束时间
    - maxRetailPrice: 零售价结束
    - minRetailPrice: 零售价开始
    - pageNum: 页码
    - pageSize: 页面大小
    - priceCatalogId: 所属类别id
    - productStatus: 商品状态 6-待生效 7-已上架 8-已下架
    - propertyRights: 产权
    - saleCompanyId: 销售主体id
    - serialNo: 商品编码
    - status: 0-待审核 1-已通过 2-未通过 3-已撤回 4-待添加 5-全部
    - title: 商品名称
    """

    url = "/mgmt/product/filiale/export"
    with client.get(url=url, params=params, headers=headers) as r:
        return r

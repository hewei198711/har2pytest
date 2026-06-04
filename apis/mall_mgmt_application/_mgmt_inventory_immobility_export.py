import os

from util.client import client

params = {
    "beginImmobilityTime": "",  # 不动库存开始时间
    "companyCode": "",  # 分公司编号
    "discountType": 0,  # 折扣类型 1:A->65%, 2:B->70%, 3:C->75%, 4:D->85%
    "endImmobilityTime": "",  # 不动库存结束时间
    "exportFileName": "",  # 导出的文件名称
    "isBadAssetStore": 0,  # 是否不良资产门店, 0->否 1->是';
    "pageNum": 0,  # 页数
    "pageSize": 0,  # 页大小
    "product": "",  # 商品关键字
    "productCode": "",  # 产品编号
    "stock": 0,  # 库存
    "stockOperator": 0,  # 库存运算符: 1为'>='，2为'>'，3为'<=',4为'<'
    "storeCode": "",  # 服务中心编号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_immobility_export(params=params, headers=headers):
    """
    excel导出库存列表(长期不动库存维度)
    /mgmt/inventory/immobility/export

    参数说明:
    - beginImmobilityTime: 不动库存开始时间
    - companyCode: 分公司编号
    - discountType: 折扣类型 1:A->65%, 2:B->70%, 3:C->75%, 4:D->85%
    - endImmobilityTime: 不动库存结束时间
    - exportFileName: 导出的文件名称
    - isBadAssetStore: 是否不良资产门店, 0->否 1->是';
    - pageNum: 页数
    - pageSize: 页大小
    - product: 商品关键字
    - productCode: 产品编号
    - stock: 库存
    - stockOperator: 库存运算符: 1为'>='，2为'>'，3为'<=',4为'<'
    - storeCode: 服务中心编号
    """

    url = "/mgmt/inventory/immobility/export"
    with client.get(url=url, params=params, headers=headers) as r:
        return r

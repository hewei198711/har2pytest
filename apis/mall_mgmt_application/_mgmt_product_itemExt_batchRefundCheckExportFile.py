import os

from util.client import client

params = {
    "catalogId": "",  # 类型id
    "isRefundCheck": 0,  # 退款申请校验:0-禁用,1启用
    "keyword": "",  # 商品的编码或名称关键字
    "pageNum": 0,  # 页码
    "pageSize": 0,  # 页面大小
    "productStatus": 0,  # 产品状态:7-已上架，8-已下架
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_product_itemExt_batchRefundCheckExportFile(params=params, headers=headers):
    """
    退款产品配置批量导出--文件流方式
    /mgmt/product/itemExt/batchRefundCheckExportFile

    参数说明:
    - catalogId: 类型id
    - isRefundCheck: 退款申请校验:0-禁用,1启用
    - keyword: 商品的编码或名称关键字
    - pageNum: 页码
    - pageSize: 页面大小
    - productStatus: 产品状态:7-已上架，8-已下架
    """

    url = "/mgmt/product/itemExt/batchRefundCheckExportFile"
    with client.get(url=url, params=params, headers=headers) as r:
        return r

import os

from util.client import client

params = {
    "adjustTimeBegin": 0,  # 调整时间
    "adjustTimeEnd": 0,  # 调整时间
    "companyCode": "",  # 分公司编号
    "orderNo": "",  # 单据号
    "orderType": 0,  # 单据类型：1.押货单，2.押货退货单
    "pageNum": 0,  # 页数
    "pageSize": 0,  # 页大小
    "productCode": "",  # 产品编码
    "storeCode": "",  # 服务中心编号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_split_statement_export(params=params, headers=headers):
    """
    导出查询库存拆分报表
    /mgmt/inventory/split/statement-export

    参数说明:
    - adjustTimeBegin: 调整时间
    - adjustTimeEnd: 调整时间
    - companyCode: 分公司编号
    - orderNo: 单据号
    - orderType: 单据类型：1.押货单，2.押货退货单
    - pageNum: 页数
    - pageSize: 页大小
    - productCode: 产品编码
    - storeCode: 服务中心编号
    """

    url = "/mgmt/inventory/split/statement-export"
    with client.get(url=url, params=params, headers=headers) as r:
        return r

import os

from util.client import client

params = {
    "combineBegin": 0,  # 组合开始时间
    "combineEnd": 0,  # 组合结束时间
    "combineState": 0,  # 组合状态：1未组合、2已组合
    "companyCode": "",  # 分公司编号
    "pageNum": 0,  # 页数
    "pageSize": 0,  # 页大小
    "productCode": "",  # 产品编号
    "storeCode": "",  # 服务中心编号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_combine_page(params=params, headers=headers):
    """
    分页查询套装组合列表
    /mgmt/inventory/combine/page

    参数说明:
    - combineBegin: 组合开始时间
    - combineEnd: 组合结束时间
    - combineState: 组合状态：1未组合、2已组合
    - companyCode: 分公司编号
    - pageNum: 页数
    - pageSize: 页大小
    - productCode: 产品编号
    - storeCode: 服务中心编号
    """

    url = "/mgmt/inventory/combine/page"
    with client.get(url=url, params=params, headers=headers) as r:
        return r

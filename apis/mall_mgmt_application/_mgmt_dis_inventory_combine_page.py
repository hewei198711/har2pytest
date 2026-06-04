import os

from util.client import client

params = {
    "companyCode": "",  # 分公司编号
    "pageNum": 0,  # 页数
    "pageSize": 0,  # 页大小
    "product": "",  # 产品编号/名称
    "storeCode": "",  # 服务中心编号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_dis_inventory_combine_page(params=params, headers=headers):
    """
    分页查询套装组合列表
    /mgmt/dis-inventory/combine/page

    参数说明:
    - companyCode: 分公司编号
    - pageNum: 页数
    - pageSize: 页大小
    - product: 产品编号/名称
    - storeCode: 服务中心编号
    """

    url = "/mgmt/dis-inventory/combine/page"
    with client.get(url=url, params=params, headers=headers) as r:
        return r

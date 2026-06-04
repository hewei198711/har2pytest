import os

from util.client import client

params = {
    "businessMode": 0,  # 保证金类型  1 /1:3,2/85折
    "companyCode": "",  # 分公司Code
    "endTime": "",  # 结束时间
    "pageNum": 0,  # 页数
    "pageSize": 0,  # 页大小
    "startTime": "",  # 开始时间
    "storeCode": "",  # 服务中心编号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_mortgageAmount_listMortgageAmountMaxRemitWait2Verify(params=params, headers=headers):
    """
    服务中心押货额度列表---待审核
    /mgmt/inventory/mortgageAmount/listMortgageAmountMaxRemitWait2Verify

    参数说明:
    - businessMode: 保证金类型  1 /1:3,2/85折
    - companyCode: 分公司Code
    - endTime: 结束时间
    - pageNum: 页数
    - pageSize: 页大小
    - startTime: 开始时间
    - storeCode: 服务中心编号
    """

    url = "/mgmt/inventory/mortgageAmount/listMortgageAmountMaxRemitWait2Verify"
    with client.get(url=url, params=params, headers=headers) as r:
        return r

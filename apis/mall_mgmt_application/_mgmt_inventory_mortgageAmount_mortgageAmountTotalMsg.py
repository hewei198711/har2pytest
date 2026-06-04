import os

from util.client import client

data = {
    "availableEndAmount": 0.0,  # 可用押货余额最大值
    "availableStartAmount": 0.0,  # 可用押货余额最小值
    "companyCode": "",  # 分公司code
    "companyCodes": [],  # 用户所属分公司codes
    "endAmount": 0.0,  # 押货额度最大值
    "pageNum": 0,  # 第几页
    "pageSize": 0,  # 每页显示页数
    "searchIsAll": False,  # 是否查询全部 标识 true 是   其他 否
    "startAmount": 0.0,  # 押货额度最小值
    "storeCode": "",  # 服务中心code
    "storeName": "",  # 服务中心name
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_mortgageAmount_mortgageAmountTotalMsg(data=data, headers=headers):
    """
    服务中心账款管理 -- 统计综合信息
    /mgmt/inventory/mortgageAmount/mortgageAmountTotalMsg

    参数说明:
    - availableEndAmount: 可用押货余额最大值
    - availableStartAmount: 可用押货余额最小值
    - companyCode: 分公司code
    - companyCodes: 用户所属分公司codes
    - endAmount: 押货额度最大值
    - pageNum: 第几页
    - pageSize: 每页显示页数
    - searchIsAll: 是否查询全部 标识 true 是   其他 否
    - startAmount: 押货额度最小值
    - storeCode: 服务中心code
    - storeName: 服务中心name
    """

    url = "/mgmt/inventory/mortgageAmount/mortgageAmountTotalMsg"
    with client.post(url=url, json=data, headers=headers) as r:
        return r

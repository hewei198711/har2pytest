import os

from util.client import client

data = {
    "billEndMonth": 0,  # 对账单结束月份，格式：yyyyMM
    "billStartMonth": 0,  # 对账单开始月份，格式：yyyyMM
    "billType": 0,  # 对账单类型，1/实时，2/月结
    "closeCreditAmount": 0,  # 是否有信用额：0/全部，1/有，2/无
    "companyCode": "",  # 分公司编号
    "companyCustomerId": "",  # 公司签署人法大大客户编号(必填)
    "companySignPerson": "",  # 公司签署人OA工号(必填)
    "currentOperatorName": "",  # 当前操作人名称
    "isFilterShopType": 0,  # 是否过滤网点类型（默认值为1）：0/否，1/是
    "memberCardNo": "",  # 会员卡号
    "signEndDate": "",  # 签署结束日期，格式：yyyy-MM-dd
    "signStartDate": "",  # 签署开始日期，格式：yyyy-MM-dd
    "signType": 0,  # 对账单签署类型，1/1:3库存对账单，2/85%库存对账单，3/85%账款对账单，4/钱包对账单
    "storeCode": "",  # 服务中心编号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_contract_sameList(data=data, headers=headers):
    """
    相同对账单记录
    /mgmt/store/contract/sameList

    参数说明:
    - billEndMonth: 对账单结束月份，格式：yyyyMM
    - billStartMonth: 对账单开始月份，格式：yyyyMM
    - billType: 对账单类型，1/实时，2/月结
    - closeCreditAmount: 是否有信用额：0/全部，1/有，2/无
    - companyCode: 分公司编号
    - companyCustomerId: 公司签署人法大大客户编号(必填)
    - companySignPerson: 公司签署人OA工号(必填)
    - currentOperatorName: 当前操作人名称
    - isFilterShopType: 是否过滤网点类型（默认值为1）：0/否，1/是
    - memberCardNo: 会员卡号
    - signEndDate: 签署结束日期，格式：yyyy-MM-dd
    - signStartDate: 签署开始日期，格式：yyyy-MM-dd
    - signType: 对账单签署类型，1/1:3库存对账单，2/85%库存对账单，3/85%账款对账单，4/钱包对账单
    - storeCode: 服务中心编号
    """

    url = "/mgmt/store/contract/sameList"
    with client.post(url=url, json=data, headers=headers) as r:
        return r

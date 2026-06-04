import os

from util.client import client

params = {
    "changeRecord": 0,  # 变更记录 null:全部  1:存在  2:不存在
    "companyCode": "",  # 分公司编号
    "endDay": "",  # 到期日期(结束)  格式yyyy-MM-dd
    "endMonth": "",  # 审核月份 结束月份 yyyy-MM
    "moneyType": 0,  # 金额类型  null:全部   1:金额>0  2:金额=0
    "pageNum": 0,  # TODO: 添加参数说明
    "pageSize": 0,  # TODO: 添加参数说明
    "startDay": "",  # 到期日期(开始)  格式yyyy-MM-dd
    "startMonth": "",  # 审核月份 开始月份 yyyy-MM
    "storeCode": "",  # 服务中心编号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_mortgageAmount_exportMortgageAmountCredit(params=params, headers=headers):
    """
    服务中心信誉额导出
    /mgmt/inventory/mortgageAmount/exportMortgageAmountCredit

    参数说明:
    - changeRecord: 变更记录 null:全部  1:存在  2:不存在
    - companyCode: 分公司编号
    - endDay: 到期日期(结束)  格式yyyy-MM-dd
    - endMonth: 审核月份 结束月份 yyyy-MM
    - moneyType: 金额类型  null:全部   1:金额>0  2:金额=0
    - startDay: 到期日期(开始)  格式yyyy-MM-dd
    - startMonth: 审核月份 开始月份 yyyy-MM
    - storeCode: 服务中心编号
    """

    url = "/mgmt/inventory/mortgageAmount/exportMortgageAmountCredit"
    with client.get(url=url, params=params, headers=headers) as r:
        return r

import os

from util.client import client

params = {
    "companyCode": "",  # 分公司code
    "dealType": [],  # 交易类型 1、汇押货款 2、退押货款、3、其他、4、不影响押货保证金  5、押货保证金转移
    "handleType": 0,  # 手工/自动类型  1、自动处理  2、手工处理
    "inputEndTime": "",  # 录入结束时间(格式yyyy-MM-dd)
    "inputStartTime": "",  # 录入开始时间(格式yyyy-MM-dd)
    "pageNum": 0,  # 第几页
    "pageSize": 0,  # 每页显示页数
    "payAccountBankName": "",  # 付款银行
    "sourceType": [],  # 款项类型 1->汇押货款、3->其他、7->手工增加押货款、8->手工退押货款、9->押货保证金转移、14->无法识别款退款、15->无法识别款不处理、24->转销售
    "storeCode": "",  # 店铺编号
    "sysEndTime": "",  # 系统到账结束时间(格式yyyy-MM-dd)
    "sysStartTime": "",  # 系统到账开始时间(格式yyyy-MM-dd)
    "verifyEndTime": "",  # 审核结束时间(格式yyyy-MM-dd)
    "verifyStartTime": "",  # 审核开始时间(格式yyyy-MM-dd)
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_disBankRemit_exportSearchList(params=params, headers=headers):
    """
    85折银行流水搜索列表导出
    /mgmt/inventory/disBankRemit/exportSearchList

    参数说明:
    - companyCode: 分公司code
    - dealType: 交易类型 1、汇押货款 2、退押货款、3、其他、4、不影响押货保证金  5、押货保证金转移
    - handleType: 手工/自动类型  1、自动处理  2、手工处理
    - inputEndTime: 录入结束时间(格式yyyy-MM-dd)
    - inputStartTime: 录入开始时间(格式yyyy-MM-dd)
    - pageNum: 第几页
    - pageSize: 每页显示页数
    - payAccountBankName: 付款银行
    - sourceType: 款项类型 1->汇押货款、3->其他、7->手工增加押货款、8->手工退押货款、9->押货保证金转移、14->无法识别款退款、15->无法识别款不处理、24->转销售
    - storeCode: 店铺编号
    - sysEndTime: 系统到账结束时间(格式yyyy-MM-dd)
    - sysStartTime: 系统到账开始时间(格式yyyy-MM-dd)
    - verifyEndTime: 审核结束时间(格式yyyy-MM-dd)
    - verifyStartTime: 审核开始时间(格式yyyy-MM-dd)
    """

    url = "/mgmt/inventory/disBankRemit/exportSearchList"
    with client.get(url=url, params=params, headers=headers) as r:
        return r

import os

from util.client import client

data = {
    "bankName": "",  # 银行名称 -- 不传则全部
    "companyCode": "",  # 分公司code
    "companyCodes": [],  # 用户所属分公司codes
    "dealType": 0,  # 处理类型 1、自动处理  2、人为处理  全部则不传
    "id": 0,  # 主键id
    "inputEndTime": "",  # 录入结束时间(格式yyyy-MM-dd)
    "inputStartTime": "",  # 录入开始时间(格式yyyy-MM-dd)
    "pageNum": 0,  # 第几页
    "pageSize": 0,  # 每页显示页数
    "sourceType": 0,  # 款项类型 全部则不传  1汇押货款、2 1:3押货退款申请、3超额押货款退款、6无法识别款退款、7手工退押货款、8手工增押货款、9转销售、12其它、14钱包款与押货款互转、15、无法识别款不处理  19押货保证金转移
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


def _mgmt_inventory_remit_exportBankRemitList(data=data, headers=headers):
    """
    银行流水搜索列表导出
    /mgmt/inventory/remit/exportBankRemitList

    参数说明:
    - bankName: 银行名称 -- 不传则全部
    - companyCode: 分公司code
    - companyCodes: 用户所属分公司codes
    - dealType: 处理类型 1、自动处理  2、人为处理  全部则不传
    - id: 主键id
    - inputEndTime: 录入结束时间(格式yyyy-MM-dd)
    - inputStartTime: 录入开始时间(格式yyyy-MM-dd)
    - pageNum: 第几页
    - pageSize: 每页显示页数
    - sourceType: 款项类型 全部则不传  1汇押货款、2 1:3押货退款申请、3超额押货款退款、6无法识别款退款、7手工退押货款、8手工增押货款、9转销售、12其它、14钱包款与押货款互转、15、无法识别款不处理  19押货保证金转移
    - storeCode: 店铺编号
    - sysEndTime: 系统到账结束时间(格式yyyy-MM-dd)
    - sysStartTime: 系统到账开始时间(格式yyyy-MM-dd)
    - verifyEndTime: 审核结束时间(格式yyyy-MM-dd)
    - verifyStartTime: 审核开始时间(格式yyyy-MM-dd)
    """

    url = "/mgmt/inventory/remit/exportBankRemitList"
    with client.post(url=url, json=data, headers=headers) as r:
        return r

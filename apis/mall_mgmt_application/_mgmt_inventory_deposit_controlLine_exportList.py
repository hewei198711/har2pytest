import os

from util.client import client

params = {
    "companyCode": "",  # 分公司编号
    "createEndDay": "",  # 创建时间(结束)  格式yyyy-MM-dd
    "createStartDay": "",  # 创建时间(开始)  格式yyyy-MM-dd
    "ctrlType": "",  # 操作类型（新增/调整）
    "leaderNo": "",  # 负责人卡号
    "negativeDayNumEnd": 0,  # 负数天数(结算)
    "negativeDayNumStart": 0,  # 负数天数(开始)
    "pageNum": 0,  # TODO: 添加参数说明
    "pageSize": 0,  # TODO: 添加参数说明
    "recordStatus": 0,  # 状态 0-待生效，1-生效，2失效
    "status": 0,  # 审核状态 0-待审核，1-生效(审核通过)，2失效（审核不通过）
    "storeCode": "",  # 服务中心编号
    "verifyEndDay": "",  # 审核时间(结束)  格式yyyy-MM-dd
    "verifyStartDay": "",  # 审核时间(开始)  格式yyyy-MM-dd
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_deposit_controlLine_exportList(params=params, headers=headers):
    """
    差额管控列表导出
    /mgmt/inventory/deposit/controlLine/exportList

    参数说明:
    - companyCode: 分公司编号
    - createEndDay: 创建时间(结束)  格式yyyy-MM-dd
    - createStartDay: 创建时间(开始)  格式yyyy-MM-dd
    - ctrlType: 操作类型（新增/调整）
    - leaderNo: 负责人卡号
    - negativeDayNumEnd: 负数天数(结算)
    - negativeDayNumStart: 负数天数(开始)
    - recordStatus: 状态 0-待生效，1-生效，2失效
    - status: 审核状态 0-待审核，1-生效(审核通过)，2失效（审核不通过）
    - storeCode: 服务中心编号
    - verifyEndDay: 审核时间(结束)  格式yyyy-MM-dd
    - verifyStartDay: 审核时间(开始)  格式yyyy-MM-dd
    """

    url = "/mgmt/inventory/deposit/controlLine/exportList"
    with client.get(url=url, params=params, headers=headers) as r:
        return r

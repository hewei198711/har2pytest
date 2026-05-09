import os

from util.client import client

data = {
    "adjustRemark": "",  # 调整备注
    "commitEndDay": "",  # 提交时间(结束)  格式yyyy-MM-dd
    "commitStartDay": "",  # 提交时间(开始)  格式yyyy-MM-dd
    "companyCode": "",  # 分公司编号
    "effectEndDay": "",  # 生效时刻(结束)  格式yyyy-MM-dd
    "effectStartDay": "",  # 生效时间(开始)  格式yyyy-MM-dd
    "moneyType": 0,  # 金额类型  null:全部   1:金额>0  2:金额=0
    "pageNum": 0,  # TODO: 添加参数说明
    "pageSize": 0,  # TODO: 添加参数说明
    "returnEndDay": "",  # 归还时间(结束)  格式yyyy-MM-dd
    "returnStartDay": "",  # 归还时间(开始)  格式yyyy-MM-dd
    "storeCode": "",  # 服务中心编号
    "verifyEndDay": "",  # 审核时间(结束)  格式yyyy-MM-dd
    "verifyEndMonth": 0,  # 审核结束月份yyyyMM(202308)
    "verifyStartDay": "",  # 审核时间(开始)  格式yyyy-MM-dd
    "verifyStartMonth": 0,  # 审核开始月份 yyyyMM(202306)
    "verifyState": 0,  # 审核状态  null 全部  0 待审核，1 通过/待生效，2 拒绝 ，4待返还，5 已扣减
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_store_deposit_creditCtrlLog(data=data, headers=headers):
    """
    85%信誉额调整历史
    /appStore/store/deposit/creditCtrlLog

    参数说明:
    - adjustRemark: 调整备注
    - commitEndDay: 提交时间(结束)  格式yyyy-MM-dd
    - commitStartDay: 提交时间(开始)  格式yyyy-MM-dd
    - companyCode: 分公司编号
    - effectEndDay: 生效时刻(结束)  格式yyyy-MM-dd
    - effectStartDay: 生效时间(开始)  格式yyyy-MM-dd
    - moneyType: 金额类型  null:全部   1:金额>0  2:金额=0
    - returnEndDay: 归还时间(结束)  格式yyyy-MM-dd
    - returnStartDay: 归还时间(开始)  格式yyyy-MM-dd
    - storeCode: 服务中心编号
    - verifyEndDay: 审核时间(结束)  格式yyyy-MM-dd
    - verifyEndMonth: 审核结束月份yyyyMM(202308)
    - verifyStartDay: 审核时间(开始)  格式yyyy-MM-dd
    - verifyStartMonth: 审核开始月份 yyyyMM(202306)
    - verifyState: 审核状态  null 全部  0 待审核，1 通过/待生效，2 拒绝 ，4待返还，5 已扣减
    """

    url = "/appStore/store/deposit/creditCtrlLog"
    with client.post(url=url, json=data, headers=headers) as r:
        return r

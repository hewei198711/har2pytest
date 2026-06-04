import os

from util.client import client

data = {
    "creditStagesCode": "",  # 信用额分期编码
    "from": 0,  # TODO: 添加参数说明
    "pageNum": 0,  # 页数
    "pageSize": 0,  # 每页显示数
    "version": 0.0,  # 当前版本信息编号 示例 1.04
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_fin_wallet_credit_stages_queryCreditStagesDtlOperateLogData(data=data, headers=headers):
    """
    信用分期管理详情查询(操作日志)
    /mgmt/fin/wallet/credit/stages/queryCreditStagesDtlOperateLogData

    参数说明:
    - creditStagesCode: 信用额分期编码
    - pageNum: 页数
    - pageSize: 每页显示数
    - version: 当前版本信息编号 示例 1.04
    """

    url = "/mgmt/fin/wallet/credit/stages/queryCreditStagesDtlOperateLogData"
    with client.post(url=url, json=data, headers=headers) as r:
        return r

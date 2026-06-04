import os

from util.client import client

params = {
    "endTime": "",  # 提交时间结束时间
    "leaderNo": "",  # 负责人卡号
    "pageNum": 0,  # 当前页,默认第1页
    "pageSize": 0,  # 每页显示数,默认10条
    "startTime": "",  # 提交时间开始时间
    "storeCode": "",  # 店铺code
    "storeName": "",  # 服务中心名称
    "type": 0,  # 保证金类型1、 开店保证金  2 、超额保证金
    "verifyStatus": "",  # 审核状态，多个用逗号分隔 1审核通过 2已驳回 3待审核 4已取消
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_getDepositApplyList(params=params, headers=headers):
    """
    保证金申请列表
    /mgmt/store/getDepositApplyList

    参数说明:
    - endTime: 提交时间结束时间
    - leaderNo: 负责人卡号
    - pageNum: 当前页,默认第1页
    - pageSize: 每页显示数,默认10条
    - startTime: 提交时间开始时间
    - storeCode: 店铺code
    - storeName: 服务中心名称
    - type: 保证金类型1、 开店保证金  2 、超额保证金
    - verifyStatus: 审核状态，多个用逗号分隔 1审核通过 2已驳回 3待审核 4已取消
    """

    url = "/mgmt/store/getDepositApplyList"
    with client.get(url=url, params=params, headers=headers) as r:
        return r

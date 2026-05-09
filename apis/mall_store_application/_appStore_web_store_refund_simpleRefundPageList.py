import os

from util.client import client

data = {
    "applyEndTime": "",  # 申请结束时间  yyyy-MM-dd
    "applyStartTime": "",  # 申请开始时间  yyyy-MM-dd
    "pageNum": 0,  # 第几页
    "pageSize": 0,  # 页数
    "storeCode": "",  # 服务中心编号
    "verifyStatus": 0,  #  审核状态  不传则全部 0-> 待审核  1->审核通过  2->已驳回  3-> 已取消 4 -> 已退款
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_web_store_refund_simpleRefundPageList(data=data, headers=headers):
    """
    指定服务中心退款分页列表
    /appStore/web/store/refund/simpleRefundPageList

    参数说明:
    - applyEndTime: 申请结束时间  yyyy-MM-dd
    - applyStartTime: 申请开始时间  yyyy-MM-dd
    - pageNum: 第几页
    - pageSize: 页数
    - storeCode: 服务中心编号
    - verifyStatus:  审核状态  不传则全部 0-> 待审核  1->审核通过  2->已驳回  3-> 已取消 4 -> 已退款
    """

    url = "/appStore/web/store/refund/simpleRefundPageList"
    with client.post(url=url, json=data, headers=headers) as r:
        return r

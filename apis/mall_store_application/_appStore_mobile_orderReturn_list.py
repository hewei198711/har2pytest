import os

from util.client import client

params = {
    "from": 0,  # TODO: 添加参数说明
    "pageNum": 0,  # 页数
    "pageSize": 0,  # 每页显示数
    "returnStatus": 0,  # 服务状态  1->待审核 2->待退回 3->待验货 98->已取消 99->已完成
    "searchKeyword": "",  # 搜索关键词
    "tabType": 0,  # 店交付 1->店交付 2->顾客自购店交付；不传就默认全部
    "waitAuditType": 0,  # 待审核类型  1->待服务中心审核 2->待分公司审核
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_mobile_orderReturn_list(params=params, headers=headers):
    """
    售后列表
    /appStore/mobile/orderReturn/list

    参数说明:
    - pageNum: 页数
    - pageSize: 每页显示数
    - returnStatus: 服务状态  1->待审核 2->待退回 3->待验货 98->已取消 99->已完成
    - searchKeyword: 搜索关键词
    - tabType: 店交付 1->店交付 2->顾客自购店交付；不传就默认全部
    - waitAuditType: 待审核类型  1->待服务中心审核 2->待分公司审核
    """

    url = "/appStore/mobile/orderReturn/list"
    with client.get(url=url, params=params, headers=headers) as r:
        return r

import os

from util.client import client

data = {
    "bankName": "",  # 银行名称 -- 不传则全部
    "companyCode": "",  # 分公司code
    "dealStatus": 0,  # 处理状态 0 待处理  1 已处理  2 -> 不处理
    "id": 0,  # 主键id
    "pageNum": 0,  # 第几页
    "pageSize": 0,  # 每页显示页数
    "sourceType": 0,  # 款项类型 全部则不传 5无法识别款确认押货款、6无法识别款退款 、15无法识别款不处理
    "storeCode": "",  # 店铺编号
    "sysEndTime": "",  # 系统到账结束时间
    "sysStartTime": "",  # 系统到账开始时间
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_remit_unknownRemit_pageList(data=data, headers=headers):
    """
    未知款项流水分页搜索列表
    /mgmt/inventory/remit/unknownRemit/pageList

    参数说明:
    - bankName: 银行名称 -- 不传则全部
    - companyCode: 分公司code
    - dealStatus: 处理状态 0 待处理  1 已处理  2 -> 不处理
    - id: 主键id
    - pageNum: 第几页
    - pageSize: 每页显示页数
    - sourceType: 款项类型 全部则不传 5无法识别款确认押货款、6无法识别款退款 、15无法识别款不处理
    - storeCode: 店铺编号
    - sysEndTime: 系统到账结束时间
    - sysStartTime: 系统到账开始时间
    """

    url = "/mgmt/inventory/remit/unknownRemit/pageList"
    with client.post(url=url, json=data, headers=headers) as r:
        return r

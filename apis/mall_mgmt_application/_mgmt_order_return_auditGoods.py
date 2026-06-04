import os

from util.client import client

data = {
    "attachmentUrlList": [],  # 审核附件URL列表
    "auditGoodsText": "",  # 备注
    "auditStatus": 0,  # 审核状态  1->通过 2->不通过
    "remarks": "",  # 审核意见
    "serviceNo": "",  # 售后单号
    "subsidyFreight": 0.0,  # 运费补贴
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_order_return_auditGoods(data=data, headers=headers):
    """
    退货验货审核
    /mgmt/order/return/auditGoods

    参数说明:
    - attachmentUrlList: 审核附件URL列表
    - auditGoodsText: 备注
    - auditStatus: 审核状态  1->通过 2->不通过
    - remarks: 审核意见
    - serviceNo: 售后单号
    - subsidyFreight: 运费补贴
    """

    url = "/mgmt/order/return/auditGoods"
    with client.post(url=url, json=data, headers=headers) as r:
        return r

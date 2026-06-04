import os

from util.client import client

data = {
    "attachmentUrlList": [],  # 审核附件URL列表
    "auditStatus": 0,  # 审核状态  1->通过 2->不通过
    "exchangeType": 0,  # 换货方式 1->先退后换 2->秒换 3->先换后退
    "junkHandleType": 0,  # 旧品处理方式 1->分公司处理 2->中转仓处理
    "reason1": "",  # 一级退货原因
    "reason1Id": 0,  # 一级退货原因id
    "reason1Remark": "",  # 一级退货原因备注
    "reason2": "",  # 二级退货原因
    "reason2Id": 0,  # 二级退货原因id
    "reason2Remark": "",  # 二级退货原因备注
    "remarks": "",  # 审核意见
    "serviceNo": "",  # 售后单号
    "subsidyFreight": 0.0,  # 运费补贴
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_order_return_auditOrderReturn(data=data, headers=headers):
    """
    分公司退货审核
    /mgmt/order/return/auditOrderReturn

    参数说明:
    - attachmentUrlList: 审核附件URL列表
    - auditStatus: 审核状态  1->通过 2->不通过
    - exchangeType: 换货方式 1->先退后换 2->秒换 3->先换后退
    - junkHandleType: 旧品处理方式 1->分公司处理 2->中转仓处理
    - reason1: 一级退货原因
    - reason1Id: 一级退货原因id
    - reason1Remark: 一级退货原因备注
    - reason2: 二级退货原因
    - reason2Id: 二级退货原因id
    - reason2Remark: 二级退货原因备注
    - remarks: 审核意见
    - serviceNo: 售后单号
    - subsidyFreight: 运费补贴
    """

    url = "/mgmt/order/return/auditOrderReturn"
    with client.post(url=url, json=data, headers=headers) as r:
        return r

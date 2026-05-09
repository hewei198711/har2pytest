import os

from util.client import client

params = {
    "id": "",  # 主键id
    "remark": "",  # 审核备注
    "type": "",  # 1 ->审核同意  2 ->审核驳回  3->汇款失败  4->汇款成功
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_web_store_refund_deal(params=params, headers=headers):
    """
    审核同意/驳回/汇款失败/汇款成功处理
    /appStore/web/store/refund/deal

    参数说明:
    - id: 主键id
    - remark: 审核备注
    - type: 1 ->审核同意  2 ->审核驳回  3->汇款失败  4->汇款成功
    """

    url = "/appStore/web/store/refund/deal"
    with client.get(url=url, params=params, headers=headers) as r:
        return r

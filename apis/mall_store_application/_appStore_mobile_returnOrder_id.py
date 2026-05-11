import os

from util.client import client

params = {
    "id": "page",  # TODO: 添加参数说明
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_mobile_returnOrder_id(params=params, headers=headers):
    """
    押货退货分页
    /appStore/mobile/returnOrder/{id}

    参数说明:
    - orderStatus: 押货换货处理状态 1待审核 2待退回 3待验货 4已完成 5已取消,押货退货处理状态:1待审核 2待退回 3待验货 4待发货 5待收货 6已完成 7已取消,货损货差处理状态:状态 1待审核 2待补换 3待收货 4已完成 5已取消
    - pageNum: 页数
    - pageSize: 页大小
    - searchStr: 押货退货/换货单单号/产品名称/产品编号
    """

    url = f"/appStore/mobile/returnOrder/{params['id']}"
    with client.get(url=url, headers=headers) as r:
        return r

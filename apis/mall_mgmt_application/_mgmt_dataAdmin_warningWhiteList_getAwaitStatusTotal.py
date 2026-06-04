import os

from util.client import client

params = {
    "endTime": "",  # 失效时间
    "number": "",  # (会员/门店)编号
    "pageNum": 0,  # 页码(不传默认为1)
    "pageSize": 0,  # 每页大小(不传默认为10)
    "startTime": "",  # 生效时间
    "status": "",  # 状态(0:待审核；1:审核通过；2:审核不通过；3：停止；4：删除)
    "statusList": [],  # TODO: 添加参数说明
    "type": 0,  # 类型(0:会员权限；1:门店权限)
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_dataAdmin_warningWhiteList_getAwaitStatusTotal(params=params, headers=headers):
    """
    列表待审核条数
    /mgmt/dataAdmin/warningWhiteList/getAwaitStatusTotal

    参数说明:
    - endTime: 失效时间
    - number: (会员/门店)编号
    - pageNum: 页码(不传默认为1)
    - pageSize: 每页大小(不传默认为10)
    - startTime: 生效时间
    - status: 状态(0:待审核；1:审核通过；2:审核不通过；3：停止；4：删除)
    - type: 类型(0:会员权限；1:门店权限)
    """

    url = "/mgmt/dataAdmin/warningWhiteList/getAwaitStatusTotal"
    with client.get(url=url, params=params, headers=headers) as r:
        return r

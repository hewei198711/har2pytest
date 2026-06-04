import os

from util.client import client

data = {
    "appendix": "",  # 附件
    "companyName": "",  # 操作人分公司
    "createTime": "",  # 创建时间
    "endTime": "",  # 失效时间
    "listId": 0,  # id标识
    "listIds": [],  # id标识List
    "number": "",  # (会员/门店)编号
    "operationName": "",  # 操作人姓名
    "operationStaff": "",  # 操作人账号
    "remark": "",  # 备注
    "rule": 0,  # 白名单规则(1:所有规则)
    "startTime": "",  # 生效时间
    "status": 0,  # 状态(0:待审核；1:审核通过；2:审核不通过；3：停止；4：删除)
    "type": 0,  # 类型(0:会员权限；1:门店权限)
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_dataAdmin_warningWhiteList_audit(data=data, headers=headers):
    """
    审核
    /mgmt/dataAdmin/warningWhiteList/audit

    参数说明:
    - appendix: 附件
    - companyName: 操作人分公司
    - createTime: 创建时间
    - endTime: 失效时间
    - listId: id标识
    - listIds: id标识List
    - number: (会员/门店)编号
    - operationName: 操作人姓名
    - operationStaff: 操作人账号
    - remark: 备注
    - rule: 白名单规则(1:所有规则)
    - startTime: 生效时间
    - status: 状态(0:待审核；1:审核通过；2:审核不通过；3：停止；4：删除)
    - type: 类型(0:会员权限；1:门店权限)
    """

    url = "/mgmt/dataAdmin/warningWhiteList/audit"
    with client.post(url=url, json=data, headers=headers) as r:
        return r

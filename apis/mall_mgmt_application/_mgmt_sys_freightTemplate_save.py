import os

from util.client import client

data = {
    "freightName": "",  # 名称
    "id": 0,  # 主键id
    "intervalList": [
        {"chargeAmount": 0.0, "endAmount": 0.0, "id": 0, "startAmount": 0.0, "templateId": 0}
    ],  # 运费模板收费区间
    "totalAmount": 0.0,  # 金额
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_sys_freightTemplate_save(data=data, headers=headers):
    """
    新增运费模板
    /mgmt/sys/freightTemplate/save

    参数说明:
    - freightName: 名称
    - id: 主键id
    - intervalList: 运费模板收费区间
    - intervalList.chargeAmount: 收费金额
    - intervalList.endAmount: 结束金额
    - intervalList.startAmount: 开始金额
    - intervalList.templateId: 模板id
    - totalAmount: 金额
    """

    url = "/mgmt/sys/freightTemplate/save"
    with client.post(url=url, json=data, headers=headers) as r:
        return r

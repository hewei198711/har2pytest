import os

from util.client import client

data = {
    "content": "",  # 发票内容(注:无内容时传空字符串,不要传空)
    "id": 0,  # 主键id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_sys_setInvoiceContent(data=data, headers=headers):
    """
    配置发票采集内容
    /mgmt/sys/setInvoiceContent

    参数说明:
    - content: 发票内容(注:无内容时传空字符串,不要传空)
    - id: 主键id
    """

    url = "/mgmt/sys/setInvoiceContent"
    with client.post(url=url, json=data, headers=headers) as r:
        return r

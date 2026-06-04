import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_sys_store_certificate_bath_template(headers=headers):
    """
    获取批量证件审核模板
    /mgmt/sys/store/certificate/bath/template
    """

    url = "/mgmt/sys/store/certificate/bath/template"
    with client.get(url=url, headers=headers) as r:
        return r

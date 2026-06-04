import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
}


def _mgmt_cms_cashier_linkconfig_query(headers=headers):
    """
    收银台链接配置查询信息
    /mgmt/cms/cashier/linkconfig/query
    """

    url = "/mgmt/cms/cashier/linkconfig/query"
    with client.post(url=url, headers=headers) as r:
        return r

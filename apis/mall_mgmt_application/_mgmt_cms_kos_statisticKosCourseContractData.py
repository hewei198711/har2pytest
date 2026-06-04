import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_kos_statisticKosCourseContractData(headers=headers):
    """
    数据看板-签约数据数据
    /mgmt/cms/kos/statisticKosCourseContractData
    """

    url = "/mgmt/cms/kos/statisticKosCourseContractData"
    with client.get(url=url, headers=headers) as r:
        return r

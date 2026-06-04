import os

from util.client import client

params = {
    "collectionCompanyName": "",  # collectionCompanyName
    "collectionCompanyNo": "",  # collectionCompanyNo
    "totalMoney": "",  # totalMoney
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_fin_wallet_downloadCalculationTable(params=params, headers=headers):
    """
    下载计算表
    /mgmt/fin/wallet/downloadCalculationTable

    参数说明:
    - collectionCompanyName: collectionCompanyName
    - collectionCompanyNo: collectionCompanyNo
    - totalMoney: totalMoney
    """

    url = "/mgmt/fin/wallet/downloadCalculationTable"
    with client.get(url=url, params=params, headers=headers) as r:
        return r

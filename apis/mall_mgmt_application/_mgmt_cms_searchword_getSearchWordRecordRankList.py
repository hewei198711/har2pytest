import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_searchword_getSearchWordRecordRankList(headers=headers):
    """
    获取搜索词统计记录排行
    /mgmt/cms/searchword/getSearchWordRecordRankList
    """

    url = "/mgmt/cms/searchword/getSearchWordRecordRankList"
    with client.get(url=url, headers=headers) as r:
        return r

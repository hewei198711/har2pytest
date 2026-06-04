import os

from util.client import client

params = {
    "id": 0,  # id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
}


def _mgmt_cms_classificationLabel_queryLabelById_id(params=params, headers=headers):
    """
    查询分类标签
    /mgmt/cms/classificationLabel/queryLabelById/{id}

    参数说明:
    - id: id
    """

    url = f"/mgmt/cms/classificationLabel/queryLabelById/{params['id']}"
    with client.get(url=url, headers=headers) as r:
        return r

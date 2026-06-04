import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
}


def _mgmt_cms_displayUser_importExampleExtend(headers=headers):
    """
    展示用户导入模板(卡号或手机号)
    /mgmt/cms/displayUser/importExampleExtend
    """

    url = "/mgmt/cms/displayUser/importExampleExtend"
    with client.get(url=url, headers=headers) as r:
        return r

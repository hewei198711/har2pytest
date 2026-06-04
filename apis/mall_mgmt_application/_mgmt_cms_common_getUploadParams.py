import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
}


def _mgmt_cms_common_getUploadParams(headers=headers):
    """
    获取文件上传参数
    /mgmt/cms/common/getUploadParams
    """

    url = "/mgmt/cms/common/getUploadParams"
    with client.get(url=url, headers=headers) as r:
        return r

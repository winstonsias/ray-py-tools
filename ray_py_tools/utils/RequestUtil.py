from pathlib import Path
from urllib.parse import urlencode

from requests import exceptions
from requests import request
from retrying import retry

from utils.LoggerUtil import LoggerManager

__all__ = [
    "RequestUtil"
]


class RequestUtil:
    def __init__(self, logger: LoggerManager, config: dict):
        self.log = logger
        self.proxies = config.get("proxies")
        self.timeout = config.get("timeout") or 10
        self.headers = config.get("headers")

    def wait(self):
        """
        设置网络请求间隔时间，仅对获取数据生效，不影响下载文件
        启用延时需要将第 1 ~ 2 行代码取消注释
        """

    # 随机延时
    # sleep(randint(15, 35) * 0.1)
    # 固定延时
    # sleep(2)
    # 取消延时
    pass

    def send_request_get(self, url: str, params=None, **kwargs) -> dict | bool:
        return self.send_request(url, method='get', params=params, **kwargs)

    def send_request_post(self, url: str, params=None, data: dict | None = None, **kwargs) -> dict | bool:
        return self.send_request(url, method='post', params=params, data=data, **kwargs)

    @retry(stop_max_attempt_number=3)
    def send_request(
            self,
            url: str,
            params=None,
            method='get',
            **kwargs) -> dict | bool:
        try:
            response = request(
                method,
                url,
                params=params,
                proxies=self.proxies,
                timeout=self.timeout,
                headers=self.headers, **kwargs)
            self.wait()
        except (
                exceptions.ProxyError,
                exceptions.SSLError,
                exceptions.ChunkedEncodingError,
                exceptions.ConnectionError,
        ):
            self.log.warning(f"网络异常，请求 {url}?{urlencode(params)} 失败")
            return False
        except exceptions.ReadTimeout:
            self.log.warning(f"网络异常，请求 {url}?{urlencode(params)} 超时")
            return False
        try:
            return response.json()
        except exceptions.JSONDecodeError:
            if response.text:
                self.log.warning(f"响应内容不是有效的 JSON 格式：{response.text}")
            else:
                self.log.warning("响应内容为空，可能是接口失效")
            return False


if __name__ == "__main__":
    logger1 = LoggerManager(
        main_path=Path(__file__).resolve().parent.parent,
        folder="logTest",
        name="%Y-%m-%d",
    )
    config1 = {

    }
    request1 = RequestUtil(logger1, config1)
    request1.send_request(
        url="https://www.baidu.com",
    )

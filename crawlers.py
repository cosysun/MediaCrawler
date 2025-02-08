from base.base_crawler import AbstractCrawler
from media_platform.bilibili import BilibiliCrawler
from media_platform.douyin import DouYinCrawler
from media_platform.kuaishou import KuaishouCrawler
from media_platform.tieba import TieBaCrawler
from media_platform.weibo import WeiboCrawler
from media_platform.xhs import XiaoHongShuCrawler
from media_platform.zhihu import ZhihuCrawler


class CrawlerFactory:
    CRAWLERS = {
        "xhs": XiaoHongShuCrawler,
        "dy": DouYinCrawler,
        "ks": KuaishouCrawler,
        "bili": BilibiliCrawler,
        "wb": WeiboCrawler,
        "tieba": TieBaCrawler,
        "zhihu": ZhihuCrawler
    }

    @staticmethod
    def create_crawler(platform: str) -> AbstractCrawler:
        crawler_class = CrawlerFactory.CRAWLERS.get(platform)
        if not crawler_class:
            raise ValueError(
                "Invalid Media Platform Currently only supported xhs or dy or ks or bili ...")
        return crawler_class()


class CrawlerManager:
    _crawlers = {}

    @classmethod
    def register_crawler(cls, platform_name, crawler_instance):
        cls._crawlers[platform_name] = crawler_instance

    @classmethod
    def get_crawler(cls, platform_name):
        crawler = cls._crawlers.get(platform_name)
        if not crawler:
            crawler = CrawlerFactory.create_crawler(platform_name)
            cls.register_crawler(platform_name, crawler)
        return crawler

    @classmethod
    def unregister_crawler(cls, platform_name):
        if platform_name in cls._crawlers:
            del cls._crawlers[platform_name]

# ...existing code...

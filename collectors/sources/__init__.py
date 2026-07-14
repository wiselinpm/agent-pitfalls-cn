"""各数据源适配器集合。"""

from __future__ import annotations

from typing import Iterable

from ..base import BaseCollector, RawHit


def all_collectors() -> list[BaseCollector]:
    """返回所有内置采集器实例，惰性 import 以避免无依赖时的 import error。"""
    from .github_issues import GitHubIssuesCollector
    from .github_releases import GitHubReleasesCollector
    from .rss import RSSCollector
    from .hackernews import HackerNewsCollector
    from .reddit import RedditCollector
    from .zhihu import ZhihuCollector
    from .zhihu_v2 import ZhihuV2Collector
    from .medium import MediumCollector
    from .devto import DevToCollector
    from .stackoverflow import StackOverflowCollector
    from .arxiv import ArxivCollector
    from .arxiv_v2 import ArxivV2Collector
    from .awesome import AwesomeCollector
    # 国内
    from .juejin import JuejinCollector
    from .juejin_v2 import JuejinV2Collector
    from .segmentfault import SegmentFaultCollector
    from .infoq_cn import InfoQCNCollector
    from .cnblogs import CnblogsCollector
    from .csdn import CSDNCollector
    from .oschina import OSChinaCollector
    from .meituan import MeituanCollector
    from .sspai import SspaiCollector
    from .cloud_cn import CloudCNCollector
    from .sogou_wechat import SogouWeChatCollector
    # 国际补充
    from .lobsters import LobstersCollector
    from .huggingface import HuggingFacePapersCollector
    from .producthunt import ProductHuntCollector
    from .official_status import OfficialStatusCollector
    from .vendor_blogs import VendorBlogsCollector
    from .newsletters import NewslettersCollector
    from .frameworks import FrameworksCollector
    from .tldr import TLDRCollector
    from .dev_community import DevCommunityCollector
    from .forums import ForumsCollector
    from .extra_en import ExtraENCollector
    from .meta_search import MetaSearchCollector
    from .reddit_v2 import RedditV2Collector
    from .google_news import GoogleNewsCollector
    from .bilibili import BilibiliCollector
    from .weibo import WeiboCollector
    from .youtube import YouTubeCollector
    from .substack import SubstackCollector
    from .communities import CommunitiesCollector
    from .more_academic import OpenReviewCollector, PapersWithCodeCollector
    from .vendor_official import VendorOfficialCollector
    from .feed_aggregator import FeedAggregatorCollector
    from .discord_hn_reddit import (
        HackerNewsSearchCollector,
        RedditFeedCollector,
        LobstersTagsCollector,
        DevToLatestCollector,
    )
    # Round 4
    from .round4_sources import (
        ArxivCategoriesCollector,
        CnEngBlogCollector,
        GithubChangelogCollector,
        AiResearchBlogCollector,
        AiNewsletterCollector,
        HnAlgoliaExtendedCollector,
    )
    from .round4_more import (
        CnTechMediaCollector,
        RedditProxyCollector,
        DiscourseCollector,
    )
    # Round 5
    from .round5_sources import (
        SemanticScholarCollector,
        GithubTrendingCollector,
        KaggleCollector,
        HnCommentsCollector,
        TechNewsCollector,
    )
    # Round 6
    from .round6_sources import (
        DblpCollector,
        AclAnthologyCollector,
        KolBlogCollector,
        GovSecCollector,
        TwitterMirrorCollector,
        PodcastCollector,
        HfTrendingCollector,
    )
    # Round 7
    from .round7_sources import (
        StackExchangeMultiCollector,
        V2EXCollector,
        NodeSeekCollector,
        TdsCollector,
        AcmEngCollector,
        TopVenuesCollector,
        IeeeAcmCollector,
        VendorCommunityCollector,
        QuoraCollector,
        MastodonTimelineCollector,
        WechatRsshubCollector,
    )
    # Round 8
    from .round8_sources import (
        BaiduTiebaCollector,
        ZhihuColumnCollector,
        CsdnBlogCollector,
        CnblogsRssCollector,
        TencentCloudCollector,
        AliyunCollector,
        HuaweiCloudCollector,
        MediumTagCollector,
        SubstackCollectorV2,
        GithubDiscussionsV2Collector,
        TechNewsRssCollector,
        AcmRssCollector,
        UsenixLoginCollector,
        ConferencePapersCollector,
        YoutubeAiCollector,
        BilibiliAiCollector,
        RedditAiCollector,
    )

    return [
        GitHubIssuesCollector(),
        GitHubReleasesCollector(),
        RSSCollector(),
        HackerNewsCollector(),
        RedditCollector(),
        RedditV2Collector(),
        ZhihuCollector(),
        ZhihuV2Collector(),
        MediumCollector(),
        DevToCollector(),
        StackOverflowCollector(),
        ArxivCollector(),
        ArxivV2Collector(),
        AwesomeCollector(),
        # 国内
        JuejinCollector(),
        JuejinV2Collector(),
        SegmentFaultCollector(),
        InfoQCNCollector(),
        CnblogsCollector(),
        CSDNCollector(),
        OSChinaCollector(),
        MeituanCollector(),
        SspaiCollector(),
        CloudCNCollector(),
        SogouWeChatCollector(),
        # 国际补充
        LobstersCollector(),
        HuggingFacePapersCollector(),
        ProductHuntCollector(),
        OfficialStatusCollector(),
        VendorBlogsCollector(),
        NewslettersCollector(),
        FrameworksCollector(),
        TLDRCollector(),
        DevCommunityCollector(),
        ForumsCollector(),
        ExtraENCollector(),
        MetaSearchCollector(),
        GoogleNewsCollector(),
        BilibiliCollector(),
        WeiboCollector(),
        YouTubeCollector(),
        SubstackCollector(),
        CommunitiesCollector(),
        OpenReviewCollector(),
        PapersWithCodeCollector(),
        VendorOfficialCollector(),
        FeedAggregatorCollector(),
        HackerNewsSearchCollector(),
        RedditFeedCollector(),
        LobstersTagsCollector(),
        DevToLatestCollector(),
        # Round 4
        ArxivCategoriesCollector(),
        CnEngBlogCollector(),
        GithubChangelogCollector(),
        AiResearchBlogCollector(),
        AiNewsletterCollector(),
        HnAlgoliaExtendedCollector(),
        CnTechMediaCollector(),
        RedditProxyCollector(),
        DiscourseCollector(),
        # Round 5
        SemanticScholarCollector(),
        GithubTrendingCollector(),
        KaggleCollector(),
        HnCommentsCollector(),
        TechNewsCollector(),
        # Round 6
        DblpCollector(),
        AclAnthologyCollector(),
        KolBlogCollector(),
        GovSecCollector(),
        TwitterMirrorCollector(),
        PodcastCollector(),
        HfTrendingCollector(),
        # Round 7
        StackExchangeMultiCollector(),
        V2EXCollector(),
        NodeSeekCollector(),
        TdsCollector(),
        AcmEngCollector(),
        TopVenuesCollector(),
        IeeeAcmCollector(),
        VendorCommunityCollector(),
        QuoraCollector(),
        MastodonTimelineCollector(),
        WechatRsshubCollector(),
        # Round 8
        BaiduTiebaCollector(),
        ZhihuColumnCollector(),
        CsdnBlogCollector(),
        CnblogsRssCollector(),
        TencentCloudCollector(),
        AliyunCollector(),
        HuaweiCloudCollector(),
        MediumTagCollector(),
        SubstackCollectorV2(),
        GithubDiscussionsV2Collector(),
        TechNewsRssCollector(),
        AcmRssCollector(),
        UsenixLoginCollector(),
        ConferencePapersCollector(),
        YoutubeAiCollector(),
        BilibiliAiCollector(),
        RedditAiCollector(),
    ]


def safe_collect(coll: BaseCollector) -> Iterable[RawHit]:
    """统一异常处理 — 单个 source 挂掉不应阻断整批。"""
    try:
        yield from coll.collect()
    except Exception as exc:  # noqa: BLE001
        import logging

        logging.getLogger("collectors").warning(
            "collector %s failed: %s", getattr(coll, "name", coll.__class__.__name__), exc
        )
        return
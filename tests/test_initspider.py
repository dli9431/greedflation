# tests/test_initspider.py
import pytest
from scrapy.http import TextResponse
from ..spider.spiders.initspider import InitSpider

@pytest.fixture
def spider():
    return InitSpider()

def test_spider_parse(spider):
    # Create a mock response for the spider to parse
    response = TextResponse(url='http://www.example.com', body=b'example response')

    # Call the spider's parse method
    results = spider.parse(response)

    # Check that the parse method returns an iterable of items or requests
    assert isinstance(results, (InitSpider, list, tuple, type(None)))
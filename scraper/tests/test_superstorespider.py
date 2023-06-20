import pytest
from scrapy.http import Response
from scrapy.spiders import Spider
from unittest.mock import MagicMock, patch
from ..spider.spiders.superstorespider import SuperstoreSpider

@pytest.fixture
def spider():
    return SuperstoreSpider()

def test_spider_name(spider):
    assert spider.name == 'superstore'

def test_has_been_scraped(spider):
    # Test that has_been_scraped returns False when no matching document is found
    spider.db[spider.collection_name_scraped].find_one = MagicMock(return_value=None)
    assert spider.has_been_scraped('https://example.com', {'pagination': {'from': 0, 'size': 10}}) == False

    # Test that has_been_scraped returns True when a matching document is found
    spider.db[spider.collection_name_scraped].find_one = MagicMock(return_value={'_id': '12345'})
    assert spider.has_been_scraped('https://example.com', {'pagination': {'from': 0, 'size': 10}}) == True

def test_mark_as_scraped(spider):
    # Test that mark_as_scraped inserts a new document into the database
    spider.db[spider.collection_name_scraped].insert_one = MagicMock()
    spider.mark_as_scraped('https://example.com', {'pagination': {'from': 0, 'size': 10}})
    spider.db[spider.collection_name_scraped].insert_one.assert_called_once()

@patch('superstorespider.SuperstoreSpider.parse')
def test_parse(mock_parse, spider):
    # Test that parse method is called with a valid response object
    response = Response(url='https://example.com', body=b'{}')
    spider.parse(response)
    mock_parse.assert_called_once_with(response)
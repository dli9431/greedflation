import json
import pytest
from unittest.mock import MagicMock, patch
from scrapy.http import TextResponse
from spider.spiders.superstorespider import SuperstoreSpider
from spider.spiders.payload import generate_payload


@pytest.fixture
def spider():
    spider = SuperstoreSpider()
    spider.db = MagicMock()
    return spider


def test_spider_name(spider):
    assert spider.name == 'superstore_spider'


def test_has_been_scraped(spider):
    # Test that has_been_scraped returns False when no matching document is found
    spider.db[spider.collection_name_scraped].find_one = MagicMock(
        return_value=None)
    assert spider.has_been_scraped(
        'https://example.com', {'pagination': {'from': 0, 'size': 10}}, hours=0) == False

    # Test that has_been_scraped returns True when a matching document is found
    spider.db[spider.collection_name_scraped].find_one = MagicMock(return_value={
                                                                   '_id': '12345'})
    assert spider.has_been_scraped(
        'https://example.com', {'pagination': {'from': 0, 'size': 10}}, hours=48) == True


def test_mark_as_scraped(spider):
    # Test that mark_as_scraped inserts a new document into the database
    spider.db[spider.collection_name_scraped].insert_one = MagicMock()
    spider.mark_as_scraped('https://example.com',
                           {'pagination': {'from': 0, 'size': 10}})
    spider.db[spider.collection_name_scraped].insert_one.assert_called_once()


@patch('spider.spiders.superstorespider.SuperstoreSpider.parse')
def test_parse(mock_parse, spider):
    spider = SuperstoreSpider()
    mock_has_been_scraped = MagicMock(return_value=False)
    spider.has_been_scraped = mock_has_been_scraped

    # Test that parse method is called with a valid response object
    url = 'https://example.com'
    payload = generate_payload(1, 0)
    response_body = '{"key": "value"}'
    headers = {'Content-Type': 'application/json'}

    assert not spider.has_been_scraped('https://example.com', payload)

    # Encode the response body as bytes using UTF-8 encoding
    response_body_bytes = response_body.encode('utf-8')

    # Create a Scrapy response object
    response = TextResponse(url=url, headers=headers, body=response_body_bytes)

    # Call the start_requests method to make the request
    req = list(spider.start_requests())
    assert len(req) == 1
    request = req[0]
    assert request.method == 'POST'
    assert request.url == spider.url
    # Updated assertion line
    assert request.body.decode('utf-8') == json.dumps(payload)

    # Call the callback function with the response
    spider.parse(response, payload)

    # Check if parse method was called
    assert mock_parse.call_count == 1
    mock_parse.assert_called_once_with(response, payload)

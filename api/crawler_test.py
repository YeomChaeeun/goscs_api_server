import unittest
from crawler import WebCrawler, NaverNewsCrawler
from datetime import datetime
from util import encode_euc_kr

class TestWebCrawler(unittest.TestCase):

  def test_get_soup(self):
    item_name = "엔비디아"
    NAVER_SOURCE_URL="https://finance.naver.com/news/news_search.naver?rcdate=&q={item}&x=0&y=0&sm=all.basic&pd=1&stDateStart=1997-01-01&stDateEnd={stDateEnd}"
    url = NAVER_SOURCE_URL.format(item = encode_euc_kr(item_name), stDateEnd = datetime.now().strftime("%Y-%m-%d"))
    
    _web_crawler = WebCrawler()
    soup = _web_crawler.get_soup(url)
    #print(soup)
    if not soup:
        return []
    
    try:
        # 여기에 실제 스크래핑 로직을 구현
        # 예시: 모든 링크 수집
        result = soup.find_all('dl', class_="newsList")
        #print(result)
    except Exception as e:
        print(f"Error parsing {url}: {e}")

  def test_get_news_list(self):
    print("******************test_get_news_title_list*************")
    item_name = "엔비디아"
    NAVER_SOURCE_URL="https://finance.naver.com/news/news_search.naver?rcdate=&q={item}&x=0&y=0&sm=all.basic&pd=1&stDateStart=1997-01-01&stDateEnd={stDateEnd}"
    url = NAVER_SOURCE_URL.format(item = encode_euc_kr(item_name), stDateEnd = datetime.now().strftime("%Y-%m-%d"))
    
    #_naver_news_crawler = NaverNewsCrawler()

    #data = _naver_news_crawler.get_news_list(url, count = 5)
  
  def test_news_page_parsing(self):
    print("****news page parsing****")
    item_name = "엔비디아kekekek"
    NAVER_SOURCE_URL="https://finance.naver.com/news/news_search.naver?rcdate=&q={item}&x=0&y=0&sm=all.basic&pd=1&stDateStart=1997-01-01&stDateEnd={stDateEnd}"
    url = NAVER_SOURCE_URL.format(item = encode_euc_kr(item_name), stDateEnd = datetime.now().strftime("%Y-%m-%d"))
    
    _naver_news_crawler = NaverNewsCrawler()
    _naver_news_crawler._news_page_parsing(url, page = 1000000)

    
if __name__ == "__main__":
  unittest.main()
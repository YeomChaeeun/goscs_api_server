from datetime import datetime

from .crawler import NaverNewsCrawler
from .util import encode_euc_kr

def get_news(item_name:str, item_count:int = 5):
  NAVER_SOURCE_URL="https://finance.naver.com/news/news_search.naver?rcdate=&q={item}&x=0&y=0&sm=all.basic&pd=1&stDateStart=1997-01-01&stDateEnd={stDateEnd}"

  url = NAVER_SOURCE_URL.format(item = encode_euc_kr(item_name), stDateEnd = datetime.now().strftime("%Y-%m-%d"))
  _web_crawler = NaverNewsCrawler()
  return _web_crawler.get_news_list(url, item_count)
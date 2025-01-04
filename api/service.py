from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import matplotlib.pyplot as plt
from enum import Enum
import FinanceDataReader as fdr

from .crawler import NaverNewsCrawler
from .util import encode_euc_kr

def get_news(item_name:str, item_count:int = 5):
  NAVER_SOURCE_URL="https://finance.naver.com/news/news_search.naver?rcdate=&q={item}&x=0&y=0&sm=all.basic&pd=1&stDateStart=1997-01-01&stDateEnd={stDateEnd}"

  url = NAVER_SOURCE_URL.format(item = encode_euc_kr(item_name), stDateEnd = datetime.now().strftime("%Y-%m-%d"))
  _web_crawler = NaverNewsCrawler()
  return _web_crawler.get_news_list(url, item_count)

class Duration(Enum):
  Y1 = lambda : relativedelta(years = 1)
  Y3 = lambda : relativedelta(years = 3)
  Y5 = lambda : relativedelta(years = 5)
  M1 = lambda : relativedelta(months = 1)
  M3 = lambda : relativedelta(months = 3)
  M6 = lambda : relativedelta(months = 6)
  W1 = lambda : relativedelta(weeks = 1)

  @staticmethod
  def get_duration_func(duration_str:str):
    if duration_str == 'Y1': return Duration.Y1
    if duration_str == 'Y3': return Duration.Y3
    if duration_str == 'Y5': return Duration.Y5
    if duration_str == 'M1': return Duration.M1
    if duration_str == 'M3': return Duration.M3
    if duration_str == 'M6': return Duration.M6
    if duration_str == 'W1': return Duration.W1
    return None
  

def get_adjusted_close_graph(item_code:list[str], duration_str:str = None):
  duration = Duration.get_duration_func(duration_str)
  yesterday = datetime.now() - timedelta(days=1)
  if duration:
    price_df = fdr.DataReader(", ".join(item_code), yesterday - duration(), yesterday)
  else:
    price_df = fdr.DataReader(", ".join(item_code))
  print(price_df)

  price_df.plot()
  filename = "adjusted_close/"+", ".join(item_code)+'_'+datetime.now().strftime('%Y%m%d')+".png"
  plt.savefig(fname = filename)

  return filename


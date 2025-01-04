from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import pandas as pd
import matplotlib.pyplot as plt
from enum import Enum
import FinanceDataReader as fdr
import requests as rq
from io import StringIO

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


def get_industry_marcap_pie(duration:Duration=Duration.Y1):
  yesterday = datetime.now() - timedelta(days=1)
  
  df = download_krx_sector(yesterday.strftime('%Y%m%d'))
  marcap_df = df.groupby(by = '업종명')['시가총액'].sum().reset_index(name = 'Marcap').sort_values(by = 'Marcap').set_index('업종명')
  
  wedgeprops = {'width': 0.8, 'edgecolor': 'w', 'linewidth': 2}
  marcap_df.plot.pie(y = 'Marcap', autopct = '%1.1f%%',
                   wedgeprops = wedgeprops, pctdistance = 0.8,
                   figsize = (10, 10), ylabel = '', legend = False)
  filename = "industry_marcap_pie/pie{}".format(yesterday.strftime("%Y%m%d"))
  plt.savefig(fname = filename)

  return filename

def get_krx_otp(otp_params, headers):
  krx_gen_otp_url = 'http://data.krx.co.kr/comm/fileDn/GenerateOTP/generate.cmd'

  krx_otp = rq.post(krx_gen_otp_url, otp_params, headers = headers).text
  return krx_otp

def download_krx_sector(at_date, market = None):
  if not market:
    kospi_df = download_krx_sector(at_date, 'KOSPI')
    kosdaq_df = download_krx_sector(at_date, 'KOSDAQ')
    return pd.concat([kospi_df, kosdaq_df])

  headers = { 'Referer': 'http://data.krx.co.kr/contents/MDC/MDI/mdiLoader/index.cmd?menuId=MDC0201010101&idxIndMidclssCd=02&money=1' }
  otp_params = {
      'locale': 'ko_KR',
      'trdDd': at_date,
      'share':'2',
      'money': '1',
      'csvxls_isNo': 'false',
      'name': 'fileDown',
      'url': 'dbms/MDC/STAT/standard/MDCSTAT00101'
  }
  if market == 'KOSPI':
    otp_params |= { 'idxIndMidclssCd': '02' }
  elif market == 'KOSDAQ':
    otp_params |= { 'idxIndMidclssCd': '03' }

  otp = get_krx_otp(otp_params, headers)

  download_url = 'http://data.krx.co.kr/comm/fileDn/download_csv/download.cmd'
  download_params = {
      'code': otp
  }
  res = rq.post(download_url, download_params, headers = headers)

  res.encoding = 'euc-kr'
  return pd.read_csv(StringIO(res.text))
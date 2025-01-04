from datetime import datetime
import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
from urllib.parse import parse_qs, urlparse
from datetime import datetime
import re

class WebCrawler:

    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        self.session = requests.Session()

    def get_soup(self, url):
        """URL로부터 BeautifulSoup 객체를 생성합니다."""
        try:
            response = self.session.get(url, headers=self.headers)
            response.raise_for_status()  # HTTP 에러 체크
            return BeautifulSoup(response.text, 'html.parser')
        except requests.RequestException as e:
            print(f"Error fetching {url}: {e}")
            return None
    
    def scrape_page(self, url):
        """단일 페이지를 스크래핑합니다."""
        soup = self.get_soup(url)
        if not soup:
            return []
        
        try:
            # 여기에 실제 스크래핑 로직을 구현
            # 예시: 모든 링크 수집
            links = soup.find_all('a')
            data = [{'url': link.get('href'), 'text': link.text.strip()} 
                   for link in links if link.get('href')]
            return data
        except Exception as e:
            print(f"Error parsing {url}: {e}")
            return []
    
    def scrape_with_pagination(self, base_url, start_page, end_page):
        """페이지네이션이 있는 웹사이트를 스크래핑합니다."""
        all_data = []
        
        for page in range(start_page, end_page + 1):
            url = f"{base_url}?page={page}"
            print(f"Scraping page {page}...")
            
            page_data = self.scrape_page(url)
            all_data.extend(page_data)
            
            # 과도한 요청 방지를 위한 대기
            time.sleep(1)
        
        return all_data
    
    def save_to_csv(self, data, filename=None):
        """결과를 CSV 파일로 저장합니다."""
        if not filename:
            filename = f"crawling_result_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        df = pd.DataFrame(data)
        df.to_csv(filename, index=False, encoding='utf-8-sig')
        print(f"Data saved to {filename}")

    def scrape_specific_elements(self, url, tag, class_name=None, id=None):
        """특정 태그와 클래스를 가진 요소들을 스크래핑합니다."""
        soup = self.get_soup(url)
        if not soup:
            return []
        
        try:
            if class_name:
                elements = soup.find_all(tag, class_=class_name)
            elif id:
                elements = soup.find_all(tag, id=id)
            else:
                elements = soup.find_all(tag)
            
            return [element.text.strip() for element in elements]
        except Exception as e:
            print(f"Error finding elements: {e}")
            return []

    def extract_table_data(self, url, table_class=None):
        """HTML 테이블 데이터를 추출합니다."""
        soup = self.get_soup(url)
        if not soup:
            return []
        
        try:
            if table_class:
                table = soup.find('table', class_=table_class)
            else:
                table = soup.find('table')
                
            if not table:
                return []
            
            # 헤더 추출
            headers = []
            for th in table.find_all('th'):
                headers.append(th.text.strip())
            
            # 데이터 추출
            rows = []
            for tr in table.find_all('tr')[1:]:  # 헤더 행 제외
                row = []
                for td in tr.find_all('td'):
                    row.append(td.text.strip())
                if row:  # 빈 행 제외
                    rows.append(row)
            
            return headers, rows
        except Exception as e:
            print(f"Error extracting table: {e}")
            return [], []
        
class NaverNewsCrawler(WebCrawler):
  def get_news_list(self, url, count):
    data = []
    page = 1
    while len(data)< count:
      parsing = self._news_page_parsing(url, page)
      if not parsing:
          return data
      data.extend(parsing)
      page +=1
    
    return data[:count]
    
    
  def _news_page_parsing(self, url, page = 1):
    soup = self.get_soup(url + f'&page={page}')
    if not soup:
        return []
    print(soup)
    try:
      result = soup.find_all('dl', class_="newsList")[0]
      subject_list = result.find_all(class_ = "articleSubject")
      if len(subject_list) == 0:
          print("페이지가 존재하지 않습니다.")
          return None
      summary_list = result.find_all(class_ = "articleSummary")

      data = []
      for subject, summary in zip(subject_list, summary_list):
          url = subject.a.get('href')
          if not url.startswith("https://"):
            query_params = parse_qs(urlparse(url).query)
            article_id = query_params['article_id'][0]
            office_id = query_params['office_id'][0]
            url = f"https://n.news.naver.com/mnews/article/{office_id}/{article_id}";
          article = {
              'url':url,
              'title': subject.text.strip(),
              'summary':summary.text.strip().replace('\t',''),
              'wdate':summary.find('span', class_="wdate").text.strip().replace('\t','')
          }
          print(article)
          data.append(article)

      
      return data
    except Exception as e:
        print(f"Error parsing {url}: {e}")
        return None
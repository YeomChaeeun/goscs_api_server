import unittest
import service

class TestSevice(unittest.TestCase):

  #def test_get_news(self):
  #  data = service.get_news("엔비디아", 60)
  #  print("===result===")
  #  print(len(data))

  #def test_get_graph(self):
    #service.get_graph(['229200', '0000J0'], service.Duration.M1)

  def test_get_stock_list(self):
    service.get_stock_list()

    
if __name__ == "__main__":
  if __package__ is None:
    import sys
    from os import path
    sys.path.append(path.dirname( path.dirname( path.abspath(__file__) ) ))
    
  unittest.main()
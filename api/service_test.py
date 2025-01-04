import unittest
import service

class TestSevice(unittest.TestCase):

  def test_get_news(self):
    data = service.get_news("엔비디아", 60)
    print("===result===")
    print(len(data))

    
if __name__ == "__main__":
  unittest.main()
from bes import BaseES
from bes import DefaultHandler
from bes import EBy
from bes import EKeys

class Bing(BaseES):
      def __init__(self,base_url="http://cn.bing.com/",filter_include=None,filter_exclude=None,*args,**kwargs):
            BaseES.__init__(self, base_url,*args,**kwargs)
            self._filter_include = filter_include if filter_include is None else filter_include.split(',')
            self._filter_exclude = filter_exclude if filter_exclude is None else filter_exclude.split(',')            
      
      def filter_print_href(self,element):
            print(element.get_attribute('href'))
            return True  
      
      def filter_element_by_text(self,element):
            ret_val=False
            txt = element.text
            if self._filter_include:
                  for f in self._filter_include:
                        if f in txt:
                              ret_val=True
                              break
            if self._filter_exclude:
                  for f in self._filter_exclude:
                        if f in txt:
                              ret_val=False
                              break
            return ret_val
      
      def do_search(self):
            self.find_element(EBy.CSS_SELECTOR ,'input[name=q]',lambda x:x.send_keys('东宏金融'+EKeys.RETURN))
      
      def get_element_selector(self):
            return (EBy.CSS_SELECTOR, '.b_algo a')
      
      def get_page_element(self,page):
            ps = self.find_elements(EBy.CSS_SELECTOR,'.b_pag a')
            print(page)
            for p in ps:
                  if p.text == str(page):
                        return p
                  
class BingHandler(DefaultHandler):
      def __call__(self,inst,elements):
            try:
                  for e in elements:   
                        inst.move_click(e)
            except Exception as e:
                  print(e)
                  
if __name__ == "__main__":
      bing = Bing(handler=BingHandler(),filter_include='东宏金融',filter_exclude='诈骗,入坑,虚假')
      bing.start()


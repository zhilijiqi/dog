from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from time import sleep

class BaseES:
      
      def __init__(self,base_url="http://www.baidu.com",sleep_time=1,wait_time=1,handler=None,max_page=10):
            driver = webdriver.Firefox();
            self.driver = driver
            self._base_url=base_url
            self.driver.implicitly_wait(130)

            self.sleep_time=sleep_time
            self.wait_time=wait_time
            self.page=1
            self.max_page = max_page
            self.last_url=""
            
            if handler is None:
                  handler=DefaultHandler()      
            self._handler = handler
            
            self._filter_chain = []
            for f in dir(self):
                  if f.startswith("filter") and hasattr(self,f):
                        self._filter_chain.append(getattr(self,f))
                                    

      def find_elements(self,by='id', value=None,handler=None):
            elements = self.driver.find_elements(by,value)
            if handler:
                  handler(elements)
            return elements

      
      def find_element(self,by='id', value=None, handler=None):
            element = self.driver.find_element(by,value)
            if handler:
                  handler(element)
            return element
                              
      def show_element(self,element):
            """
            检查元素是否显示
            """
            e_y = element.location.get('y',0)
            w_y = self.driver.get_window_rect().get('height',0)
            if e_y > w_y:
                  self.driver.execute_script("arguments[0].scrollIntoView();",element)

      def move_click(self,element):
            """
            鼠标移动到元素上，点击
            """
            self.show_element(element)
            driver = self.driver
            ActionChains(driver).move_to_element(element).click(element).perform()
            sleep(self.wait_time)
            cur_window = self.driver.current_window_handle       
            windows = driver.window_handles
            for w in windows:
                  if cur_window != w:
                        driver.switch_to.window(w)
                        #sleep(self.wait_time)
                        driver.close()
                        sleep(self.sleep_time)
                        driver.switch_to.window(cur_window)
                        
      #def filter_element_by_text(self,element):
            #"""
            #过滤
            #"""
            #return_value=False
            #txt = element.text
            #if self._filter_include:
                  #for f in self._filter_include:
                        #if f in txt:
                              #return_value=True
                              #break
            #if self._filter_exclude:
                  #for f in self._filter_exclude:
                        #if f in txt:
                              #return_value=False
                              #break
            #return return_value

      
      def wait_page_change(self):
            url = self.driver.current_url
            times = 20
            while times > 0 and url == self.last_url:
                  sleep(1)
                  times = times-1
                  print("wait page load times" + str(times))
            self.last_url = self.driver.current_url;
            
      def next_page(self , page=None):
            if page is None:
                  page = self.page + 1
            if page >= self.max_page:
                  return False
            p = self.get_page_element(page)
            if p is None:
                  raise TypeError("没有找到下一页")
            self.move_click(p)
            self.page = page
            return True
            #ps = self.find_elements(By.CSS_SELECTOR,'#page .pc')
            #for p in ps:
                  #if p.is_enabled and p.text == str(page):
                        #print(p.text)
                        #self.move_click(p)
                        #self.page = page
                        #return True
                  
      def get_page_element(self,page):
            msg = "没有实现."
            raise TypeError(msg)
      
      def do_search(self):
            msg = "没有实现."
            raise TypeError(msg)
      
      def get_element_selector(self):
            msg = "没有实现."
            raise TypeError(msg)
      
      @property
      def get_driver(self):
            return self.driver
      
      @property
      def base_url(self):
            return self._base_url
      
      @base_url.setter
      def base_url(self,base_url):
            self._base_url = base_url
            self.driver.get(base_url)
      
      
      #def url_load(self):
            #self.find_element(By.CSS_SELECTOR ,'input[name=wd]',lambda x:x.send_keys('东宏金融'+Keys.RETURN))
                  
      def start(self): 
            try:
                  self.base_url= self._base_url
                  self.do_search()
                  
                  while True:
                        #self.find_elements(By.CSS_SELECTOR, 'h3 a', self._call_handler)
                        self.find_elements(*self.get_element_selector(), self._call_handler)
                        if not self.next_page():
                              break
                        self.wait_page_change()
            except Exception as e:
                  raise e
            finally:
                  self.quit()
                  
      def quit(self):
            self.driver.quit()
                  
      def _call_filter_chain(self,element):
            re_val = True
            for fr in self._filter_chain:
                  if not fr(element):
                        re_val = False
                        break
            return re_val
      
      def _call_handler(self,elements):
            l = list()
            for e in elements:   
                  txt = e.text    
                  if self._call_filter_chain(e):
                        l.append(e)
            self._handler(self,l)


class DefaultHandler(object):
      def __init__(self):
            pass
      
      def __call__(self,inst,elements):
            try:
                  for e in elements:   
                        inst.move_click(e)
            except Exception as e:
                  print(e)


class EBy(By):
      pass

class EKeys(Keys):
      pass
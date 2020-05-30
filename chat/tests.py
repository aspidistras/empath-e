from channels.testing import ChannelsLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait

from django.test import Client
from django.contrib.auth.models import User


class ChatTests(ChannelsLiveServerTestCase):
    serve_static = True

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        try:
            cls.driver = webdriver.Chrome('chat/chromedriver')
        except:
            super().tearDownClass()
            raise

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def test_send_message(self):
        try:
            self.client = Client()
            self.user = User.objects.create_user(username='test', first_name='test', last_name='test',
                                                email='test@test.fr', password='test')
            self.client.login(username='test', password='test')
            
            cookie = self.client.cookies['sessionid']
            self.driver.get(self.live_server_url + '/chat/room')
            self.driver.add_cookie({'name': 'sessionid', 'value': cookie.value, 'secure': False, 'path': '/'})
            self.driver.refresh()

            self.driver.get(self.live_server_url + '/chat/room')

            self.driver.execute_script('window.open("about:blank", "_blank");')
            self.driver.switch_to_window(self.driver.window_handles[-1])
            
            self.driver.get(self.live_server_url + '/chat/room')

            self.driver.switch_to_window(self.driver.window_handles[0])

            ActionChains(self.driver).send_keys('test' + '\n').perform()

            WebDriverWait(self.driver, 2).until(lambda _:
                'test' in self.driver.find_element_by_css_selector('#chat-log').get_property('value'),
                'Message was not received by window 1 from window 1')
            
            self.driver.switch_to_window(self.driver.window_handles[1])
            
            WebDriverWait(self.driver, 2).until(lambda _:
                'test' in self.driver.find_element_by_css_selector('#chat-log').get_property('value'),
                'Message was not received by window 2 from window 1')

        finally:
            self._close_all_new_windows()


    def _close_all_new_windows(self):
        while len(self.driver.window_handles) > 1:
            self.driver.switch_to_window(self.driver.window_handles[-1])
            self.driver.execute_script('window.close();')
        if len(self.driver.window_handles) == 1:
            self.driver.switch_to_window(self.driver.window_handles[0])

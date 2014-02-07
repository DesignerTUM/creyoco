from django.test import LiveServerTestCase
from selenium import webdriver
from exeapp.tests import create_basic_database, TEST_USER, TEST_PASSWORD
import time


class IDevicesTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        create_basic_database()
        self.login()

    def login(self):
        self.browser.get(self.live_server_url + "/accounts/login/")
        self.browser.find_element_by_name("username").clear()
        self.browser.find_element_by_name("username").send_keys(TEST_USER)
        self.browser.find_element_by_name("password").clear()
        self.browser.find_element_by_name("password").send_keys(TEST_PASSWORD)
        self.browser.find_element_by_css_selector("input.login_submit").click()

    def tearDown(self):
        self.browser.quit()

    def test_multiplechoice(self):
        self.browser.find_element_by_partial_link_text("Package").click()
        self.browser.implicitly_wait(2)
        self.browser.find_elements_by_css_selector("div ul.jstree-no-dots")
        self.browser.find_elements_by_css_selector("[ideviceid='MultiChoiceIdevice']")[0].click()
        # self.browser.find_element_by_link_text("Multiple Choice").click()
        self.browser.find_element_by_id("add_term").click()
        time.sleep(1)
        self.browser.execute_script("""
        tinyMCE.editors[0].setContent("Question");
        tinyMCE.editors[1].setContent("Wrong Answer");
        tinyMCE.editors[2].setContent("Right Answer");
        """)
        self.browser.find_element_by_id("id_form-1-right_answer").click()
        self.browser.find_element_by_css_selector("form.idevice_form > input[name=\"idevice_action\"]").click()
        self.browser.find_element_by_xpath("(//input[@name='option'])[2]").click()
        self.browser.find_element_by_name("idevice_action").click()
        try:
            self.assertEqual("Correct!", self.browser.find_element_by_xpath("//div[@id='idevice1']/div/span").text)
        except AssertionError as e:
            self.verificationErrors.append(str(e))


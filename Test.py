# _*_ encoding: utf-8 _*_
"""
@Softwave: Pycharm
@Python: 3.X 
@Author: SKYNE
@Contact: 520@skyne.cn
@Time: 2017.10.16
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
# options = webdriver.ChromeOptions()
# options.add_experimental_option("excludeSwitches",["ignore-certificate-errors"])
class Erya_Course():

    def __init__(self):
        self.account = "15031310170"
        self.password = "**********"
        self.login_url = "http://passport2.chaoxing.com/login?fid=2901&refer=http://i.mooc.chaoxing.com/space/index.shtml"
        self.lession_name = []   #存储已选课程的名称
        self.user_name = ""
        self.driver = webdriver.Chrome()
        self.waiter = WebDriverWait(self.driver, 15, 1)
        self.homepage_handle = None
        self.article_name = []      #存储一个课程的所有章节名称

    def login(self):
        # 提交账号密码，验证码
        try:
            self.driver.get(self.login_url)
        except TimeoutException:
            print("网页连接超时，请检查网络！")
        self.homepage_handle = self.driver.window_handles

        # 等待三秒，等待网页加载完成
        time.sleep(3)

        # 输入学号                          #此处有坑，注意elements
        Account = self.waiter.until(
            EC.presence_of_element_located((By.ID, "unameId"))
        )
        Account.clear()
        Account.send_keys(self.account)

        # 输入密码
        Password = self.waiter.until(
            EC.presence_of_element_located((By.ID, "passwordId"))
        )
        Password.clear()
        Password.send_keys(self.password)

        # 输入验证码
        vcode_buff = input("please enter the Vcode:")
        Vcode = self.waiter.until(
            EC.presence_of_element_located((By.ID, "numcode"))
        )
        Vcode.send_keys(vcode_buff)

        # 点击登录按钮
        Login_button = self.waiter.until(
            EC.presence_of_element_located((By.CLASS_NAME, "zl_btn_right"))
        )
        Login_button.click()

        #登陆成功。提示用户
        self.user_name = self.driver.find_element_by_class_name("zt_u_name").text
        print("{}，您好，您已成功登录，正在查询课程信息，请稍后！\n".format(self.user_name))

    def Course_info(self):
        self.waiter.until(EC.frame_to_be_available_and_switch_to_it(
            (By.TAG_NAME, "iframe")))
        lession = self.driver.find_elements_by_class_name('clearfix')
        # print(type(lession))   #类型class 'selenium.webdriver.remote.webelement.WebElement'

        for name in lession:
            if name.text:  # 判断课程是否为空
                self.lession_name.append(name.text)
        # 至此，课程名称收集完毕, 但多收集了一个“已结束的课程”，从列表中去除即可
        # print(self.lession_name)
        self.lession_name.pop()
        print("您选择课程有：\n")

        for name in self.lession_name:
            print("{}\n".format(name))

    def Judge_Course_Case(self):
        for name in self.lession_name:
            print("正在查询《{}》课程的进度，请稍后！\n".format(name))
            self.waiter.until(
                EC.presence_of_element_located((By.LINK_TEXT, name))
            ).click()       # 点击课程的链接，进入课程详情页
            # print(self.driver.current_url)     出现新的窗口，需要切换至新开的窗口
            all_handles = self.driver.window_handles
            self.driver.switch_to.window(all_handles[1])    # all_handle共有两个，第一个为homepage
            article_name_buff = self.driver.find_elements_by_class_name("articlename")  # 获取所有的小节名称

            for name in article_name_buff:
                if name.text:
                    self.article_name.append(name.text)
            self.article_name.pop()         # 最后一个阅读不是视频，会导致后面，HTML元素结构不同，导致出错
            # print(self.article_name)
            self.Judge_Finish(article_name= self.article_name)

            # 判断当为最后一个章节时，切换至homepage窗口
            if name == self.article_name[-1]:
                self.driver.switch_to.window(self.homepage_handle)

    def Judge_Finish(self, article_name):      #  article_name 为所选课程所有小节的列表
            for name in article_name:
                self.waiter.until(
                    EC.presence_of_element_located((By.LINK_TEXT, name))
                ).click()
                self.waiter.until(EC.frame_to_be_available_and_switch_to_it(
                    (By.TAG_NAME, "iframe")))
                try:
                    flag = self.waiter.until(
                        EC.presence_of_element_located((By.ID, "ext-gen1038"))
                    )
                    if flag:
                        print(flag.text)
                        print("恭喜您！《{}》任务点已完成!\n".format(name))
                    else:
                        print("任务点未完成!\n")
                        print("将要执行自动播放功能，请稍等！\n")
                        self.Ctrl_Play()
                except NoSuchElementException:
                    print("出现点小错误")
                print("等待十秒，防止后台检测")
                time.sleep(10)
                self.driver.back()

    def Ctrl_Play(self):
        pass
        # self.driver.switch_to.frame(
        #     self.driver.find_element_by_tag_name("iframe"))
        # self.driver.switch_to.frame(
        #     self.driver.find_element_by_tag_name("iframe"))
        # self.driver.implicitly_wait(10)
        # reader = self.driver.find_element_by_id('reader')
        # reader.click()





if __name__ == '__main__':
    Erya = Erya_Course()
    Erya.login()
    Erya.Course_info()
    Erya.Judge_Course_Case()



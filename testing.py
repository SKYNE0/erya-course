from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.command import Command
import time

# 下面都是测试控制播放的模块，也就是直接到播放页面。


account = "15031310170"
password = "*********"
login_url = "http://passport2.chaoxing.com/login?fid=2901&refer=http://i.mooc.chaoxing.com/space/index.shtml"
lession_name = []   #存储已选课程的名称
user_name = ""
driver = webdriver.Chrome()
driver.set_window_size(960,800)
waiter = WebDriverWait(driver, 15, 1)
homepage_handle = None
article_name = []      #存储一个课程的所有章节名称


def login():
    # 提交账号密码，验证码
    try:
        driver.get(login_url)
    except TimeoutException:
        print("网页连接超时，请检查网络！")
    homepage_handle = driver.window_handles

    # 等待三秒，等待网页加载完成
    time.sleep(3)

    # 输入学号                          #此处有坑，注意elements
    Account = waiter.until(
        EC.presence_of_element_located((By.ID, "unameId"))
    )
    Account.clear()
    Account.send_keys(account)

    # 输入密码
    Password = waiter.until(
        EC.presence_of_element_located((By.ID, "passwordId"))
    )
    Password.clear()
    Password.send_keys(password)

    # 输入验证码
    vcode_buff = input("please enter the Vcode:")
    Vcode = waiter.until(
        EC.presence_of_element_located((By.ID, "numcode"))
    )
    Vcode.send_keys(vcode_buff)

    # 点击登录按钮
    Login_button = waiter.until(
        EC.presence_of_element_located((By.CLASS_NAME, "zl_btn_right"))
    )
    Login_button.click()

    # 登陆成功。提示用户
    user_name = driver.find_element_by_class_name("zt_u_name").text
    print("{}，您好，您已成功登录，正在查询课程信息，请稍后！\n".format(user_name))

    waiter.until(EC.frame_to_be_available_and_switch_to_it(
        (By.TAG_NAME, "iframe")))
    waiter.until(
        EC.presence_of_element_located((By.LINK_TEXT, "追寻幸福：中国伦理史视角"))
    ).click()

    all_handles = driver.window_handles
    driver.switch_to.window(all_handles[1])
    waiter.until(
        EC.presence_of_element_located((By.LINK_TEXT, "幸福的种类"))
    ).click()


    #  下面测试视频播放模块
    time.sleep(60)
    print("测试控制视频模块的播放")
    waiter.until(
        EC.presence_of_element_located((By.CLASS_NAME, "switchbtn"))
    ).click()
    driver.execute_script("var q=document.documentElement.scrollTop=10000")
    driver.switch_to.frame(
        driver.find_element_by_tag_name("iframe"))
    driver.switch_to.frame(
        driver.find_element_by_tag_name("iframe"))
    driver.implicitly_wait(10)

    print("将要点击事件")
    time.sleep(10)
    # 下面是试图模拟鼠标的位置以及操作，不过没反应，还未找到原因
    actions = ActionChains(driver)
    actions.move_by_offset(724,562)
    actions.click_and_hold()
    actions.perform()
    #driver.execute(Command.MOVE_TO, {'xoffset': 913, 'yoffset': 22})
    # ActionChains(driver).move_by_offset(22,913)
    # ActionChains(driver).click()
    #
    # driver.execute(Command.MOVE_TO, {'xoffset': 724, 'yoffset': 524})
    # ActionChains(driver).click_and_hold().perform()
    # # ActionChains(driver).move_by_offset(724,524).perform()
    # driver.execute(Command.MOVE_TO, {'xoffset': 724, 'yoffset': 493})
    # # ActionChains(driver).move_by_offset(724,493).perform()
    # ActionChains(driver).click_and_hold().perform()
    reader = driver.find_element_by_id('reader')
    reader.click()

if __name__ == '__main__':
    login()
    temp = input("ALL OVER!")

from selenium import webdriver
import chromedriver_autoinstaller
import time

def goDestination(target):
    url = "http://search.danawa.com/dsearch.php?k1=" + target + "&module=goods&act=dispMain"
    path = chromedriver_autoinstaller.install()
    driver = webdriver.Chrome(path)
    driver.get(url)

    time.sleep(50)

    driver.close()
    driver.quit()


if __name__ == '__main__':
    goDestination("gtx1060")
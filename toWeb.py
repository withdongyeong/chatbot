from selenium import webdriver
import chromedriver_autoinstaller
from selenium.webdriver.chrome.options import Options

def goDestination(target):
    chrom_options = Options()
    chrom_options.add_experimental_option("detach", True)

    url = "http://search.danawa.com/dsearch.php?k1=" + target + "&module=goods&act=dispMain"
    path = chromedriver_autoinstaller.install()
    driver = webdriver.Chrome(path)
    driver.get(url)

if __name__ == '__main__':
    goDestination("gtx1060")
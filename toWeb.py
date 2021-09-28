from selenium import webdriver
import chromedriver_autoinstaller
import time

def goDestination(label : int):
    url_list = dict()

    with open('destination.txt', 'r', encoding='UTF-8') as file:
        lines = file.readlines()
        for line in lines:
            temp_line = line.split(' ')
            key = int(temp_line[0])
            url = temp_line[1]
            url_list[key] = url

    print(url_list[label])

    path = chromedriver_autoinstaller.install()
    print(path)
    driver = webdriver.Chrome(path)
    driver.get(url_list[label])

    time.sleep(50)

    driver.close()
    driver.quit()


if __name__ == '__main__':
    goDestination(1)
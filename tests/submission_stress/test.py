import argparse

parser = argparse.ArgumentParser()


parser.add_argument('--email', type=str, required=True)
parser.add_argument('--password', type=str, required=True)
parser.add_argument('--host', type=str, required=True)
parser.add_argument('--problem_id', type=int, required=True)
parser.add_argument('--post_count', type=int, required=True)

args = parser.parse_args()
args_dict = vars(args)


import threading
from time import time

from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

URL = {
    'login': '/users/login/',
    'create_submission': '/problems/%d/submissions/create/' % args.problem_id,
}

URL = {
    key: args.host + val
    for key, val in URL.items()
}


def login(driver: Chrome):
    driver.get(URL['login'])
    driver.execute_script(
        '''
        $('input[name="email"]').val('{email}');
        $('input[name="password"]').val('{password}');
        $('form').submit();
        '''
        .format(**args_dict)
    )


def test(id):
    driver = Chrome(service=Service(ChromeDriverManager().install()))

    login(driver)

    driver.get(URL['create_submission'])
    driver.execute_script(
        '''
        submission('id-editor-form', getEditorData());
        '''
    )

    start = time()
    try:
        WebDriverWait(driver, 20).until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, '#id-result-detail')
        ))
    except:
        pass
    end = time()

    results[id] = {
        'time': (end - start) * 1000
    }


results = {}


if __name__ == '__main__':
    threads = []
    for i in range(args.post_count):
        threads.append(
            threading.Thread(target=test, args=[i])
        )
    
    for t in threads:
        t.start()
    
    for t in threads:
        t.join()

    print('최장 시간: %d', max(results.values(), key=lambda result: result['time']))

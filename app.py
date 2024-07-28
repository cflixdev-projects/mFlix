from selenium.webdriver.support import expected_conditions as EC
from flask import Flask, render_template, request
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait

app = Flask(__name__)



# Initialize the WebDriver instance outside of the Flask application context
options = Options()
options.add_argument("--headless")
options.add_argument('log-level=3')
driver = webdriver.Chrome(options=options)

def get_new_link_from_redirect(driver, redirect_url):
    driver.get(redirect_url)
    new_link = driver.current_url
    print('aktueller neuere link ' + new_link)
    return new_link

def get_video_link(driver, show_name):
    link = f"https://cinemathek.net/filme/{show_name}"
    driver.get(link)
    iframe_element = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'iframe.metaframe'))
    )

    # Extract the src attribute from the iframe element
    src_url = iframe_element.get_attribute('src')
    print(f'The src URL of the iframe is: {src_url}')
    return src_url

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    text_input = request.form['textInput'].replace(' ', '')
    show_name = text_input.strip()
    print(show_name)
    print(show_name)

    redirect_url = get_video_link(driver, show_name)
    new_url = get_new_link_from_redirect(driver, redirect_url)
    return new_url



if __name__ == '__main__':
    app.run(debug=True)

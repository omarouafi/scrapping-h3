import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import mysql.connector
import json
import requests
import json
import math

def initialize_driver():
    options = Options()
    options.add_argument("--disable-extensions")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--no-sandbox")
    

    driver_path = ChromeDriverManager().install()
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service, options=options)
     
    return driver


def goToPage(driver, url):
    driver.get(url)
    time.sleep(5)
    body = driver.find_element(By.TAG_NAME, 'body')
    soup = BeautifulSoup(body.get_attribute('innerHTML'), 'html.parser')
    return soup



def init_db():
    try:
        with open('config.json') as f:
            config = json.load(f)

        conn = mysql.connector.connect(
            host=config['host'],
            user=config['user'],
            password=config['password'],
            database=config['database']
        )

        cursor = conn.cursor()

        create_table_query = """CREATE TABLE IF NOT EXISTS models (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            description TEXT NOT NULL,
            image TEXT NOT NULL,
            number_of_runs FLOAT NULL
        )"""

        cursor.execute(create_table_query)

        conn.commit()

        return conn

    except Exception as e:
        print(f"Error: {e}")
        return None
    


def insert_model(engine, model_name, model_description, model_example_images,number_of_runs):
    try:
        query = f"INSERT INTO models (name, description, image, number_of_runs) VALUES ('{model_name}', '{model_description}', '{model_example_images}', '{number_of_runs}')"
        cursor = engine.cursor()    
        cursor.execute(query)
        engine.commit()
        cursor.close()
        print(f"Model {model_name} inserted successfully")
    except Exception as e:
        print(f"Error: {e}")
        engine.rollback()
    finally:
        cursor.close()
        engine.close()



def get_text_to_image_models(model_soup):
    model_name = model_soup.select_one('h3').text.strip()
    model_description = model_soup.select_one('p.mt-1.max-w-xl').text.strip()
    model_examples = model_soup.select('div.mb-2lh.h-40.overflow-hidden div img')
    model_number_of_runs_element = model_soup.select_one('span:contains("runs")')

    if model_number_of_runs_element:
        model_number_of_runs_text = model_number_of_runs_element.text
        number_of_runs_unit = model_number_of_runs_text.split(" ")[0][-2]
        model_number_of_runs = model_number_of_runs_text.split(" ")[0][:-2]

        if not math.isnan(float(model_number_of_runs)):
            model_number_of_runs = float(model_number_of_runs)
            if number_of_runs_unit == "K":
                model_number_of_runs *= 1000
            elif number_of_runs_unit == "M":
                model_number_of_runs *= 1000000
        else:
            model_number_of_runs = None
    else:
        model_number_of_runs = None

    images_src = [img['data-src'] for img in model_examples]
    print(model_number_of_runs)
    return model_name, model_description, images_src, model_number_of_runs

def main():
    driver = initialize_driver()
    domain = "https://replicate.com"
    url = '/collections/text-to-image'
    url = f'{domain}{url}'
    soup = goToPage(driver, url)
    time.sleep(10)
    models_list = soup.select('div.grid.grid-cols-1.lg\:grid-cols-2.grid-flow-row.auto-rows-max.gap-8 a')
    
    for model in models_list:
        model_url = f'{domain}{model["href"]}'
        model_soup = goToPage(driver, model_url)
        time.sleep(10)

        model_name, model_description, model_example_images,model_number_of_runs = get_text_to_image_models(model_soup)
        model_example_images = ",".join(model_example_images)
        engine = init_db()
        insert_model(engine, model_name, model_description, model_example_images)


    driver.quit()

def download_image(image_url, output_dir):
    try:
        response = requests.get(image_url)
        image_name = image_url.split("/")[-1] + "-" + str(time.time()) + ".png"
        with open(f'{output_dir}{image_name}', 'wb') as image_file:
            image_file.write(response.content)
        print(f"Image {image_name} downloaded successfully")
    except Exception as e:
        print(f"Error: {e}")
        print(f"Error downloading image {image_url}")


def generate_image(prompt):
    
    driver = initialize_driver()
    domain = "https://replicate.com"
    url = '/collections/text-to-image'
    url = f'{domain}{url}'
    soup = goToPage(driver, url)
    time.sleep(10)
    models_list = soup.select('div.grid.grid-cols-1.lg\:grid-cols-2.grid-flow-row.auto-rows-max.gap-8 a')
    
    for model in models_list:
        try :
            model_url = f'{domain}{model["href"]}'
            model_soup = goToPage(driver, model_url)
            prompt_input = driver.find_element(By.ID, 'prompt')
            prompt_input.clear()
            if prompt_input:
                
                prompt_input.send_keys(prompt)
                time.sleep(5)
                generate_button = driver.find_element(By.CSS_SELECTOR , 'button[type="submit"]')
                generate_button.click()
                time.sleep(20)
                output_image = driver.find_element(By.CSS_SELECTOR, '[data-testid="value-output-image"]')  
                image_url = output_image.get_attribute('src')
                download_image(image_url, "output/")
                print(f"Image generated successfully for model {model['href']}")
        except Exception as e:
            print(f"Error: {e}")
            print(f"Error generating image for model {model['href']}")
            continue

    driver.quit()

# generate_image("A small bird with a red head and a white belly")
main()
    
# init_db()
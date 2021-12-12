import yaml
from selenium import webdriver
from selenium.common.exceptions import ElementNotInteractableException
import sqlite3

# Connect to database
conn = sqlite3.connect('covid.db')
cursor = conn.cursor()

# Create run table, if it doesn't exist
cursor.execute("CREATE TABLE IF NOT EXISTS run (run_id INTEGER PRIMARY KEY AUTOINCREMENT, run_date DATETIME NOT NULL);")

try:
    # Let's see if this has been run yet for today
    cursor.execute("SELECT run_id, run_date FROM run WHERE run_date >= DATE('now','localtime') ORDER BY run_date LIMIT 1;")
    rs = cursor.fetchone()

    # we didn't run today, let's get started
    if not rs:  
        conf = yaml.safe_load(open('auto_ack_credentials.yaml'))
        url = conf['safe2work_user']['url']
        email = conf['safe2work_user']['email']
        password = conf['safe2work_user']['password']
        driver = webdriver.Chrome()

        def login(url,usernameId, username, passwordId, password, submit_button_class):
            driver.get(url)
            driver.find_element_by_id(usernameId).send_keys(username)
            driver.find_element_by_id(passwordId).send_keys(password)
            driver.find_element_by_css_selector(submit_button_class).click()

        login(url, 
            "UserName", email, 
            "Password", password, 
            ".validateAndSubmit")

        # Wait until "No" button is clickable
        try :
            driver.implicitly_wait(8)
            driver.find_element_by_id("BacktoLeaveRequest").click()
        # That window won't be visible if you've already confirmed
        except ElementNotInteractableException:
            pass

        # Let's quit
        driver.quit()

        # Let's only keep 2 weeks of data in our run table
        cursor.execute("DELETE FROM run WHERE run_date < DATE('now','localtime', '-14 days');")

        # Finally, let's record an entry for today
        cursor.execute("INSERT INTO run(run_date) VALUES( DATETIME('now','localtime') );")

    else:
        print("You already ran this today at", rs[1])
        print("\n")

    conn.commit()
except:
   # Rollback in case there is any error
   conn.rollback()

cursor.close()
conn.close()

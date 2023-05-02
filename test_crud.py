
import pytest
import time
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

f = open("login.txt", "r")
lines = f.readlines()
f.close()
email = lines[0].strip('\n')
password = lines[1]

class Test(unittest.TestCase):
  @classmethod
  def setUpClass(self):
    self.driver = webdriver.Chrome()
    self.driver.maximize_window()
    self.vars = {}
  @classmethod
  def tearDownClass(self):
    self.driver.quit()


  def waitForClickable(self, xpath):
    self.driver.execute_script("arguments[0].click();", WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH,
        xpath))))
  
  def goToJobList(self):
    self.driver.get("https://app.clicktime.com/App/ListView/Job/")

  def login(self, email, password):
    self.driver.get("https://login.clicktime.com")
    self.driver.find_element(By.ID, "email").click()
    self.driver.find_element(By.ID, "email").send_keys(email)
    self.driver.find_element(By.ID, "password").click()
    self.driver.find_element(By.ID, "password").send_keys(password)
    self.driver.find_element(By.ID, "loginbutton").click()
    self.driver.find_element(By.ID, "username")

  def create(self):
    self.driver.get('https://app.clicktime.com/App/Details/Job/#/entityDetail')
    self.driver.implicitly_wait(1)
    self.driver.find_element(By.ID, "edit-job-client").click()
    self.driver.find_element(By.ID, "ui-select-choices-row-0-0").click()  #choose by client name and make client name a variable
    self.driver.find_element(By.ID, "edit-job-name").click()
    self.driver.find_element(By.ID, "edit-job-name").send_keys("Projecttest") #capture time stamp and use variable for project name
    self.driver.find_element(By.ID, "edit-job-number").click()
    self.driver.find_element(By.ID, "edit-job-number").send_keys("123")
    self.driver.find_element(By.CLASS_NAME, "btn-success").click()
    self.driver.implicitly_wait(1)
    self.driver.find_element(By.XPATH, "//button[@ng-click='saveEntityAndFinish(detailDataForm)']").click()
    #confirm success message
    time.sleep(1)
    self.driver.find_element(By.XPATH, '//*[@id="ext-gen125"]')

  def update(self):
    self.driver.find_element(By.XPATH, "//tr[contains(.,'Projecttest')]//a[contains(@href,'Job')]").click() #pass string
    self.waitForClickable("//button[@id='BasicInfoTemplate-btn-edit']")
    self.waitForClickable("//*[@id='read-job-accountid']")
    #update all properties
    self.driver.implicitly_wait(1)
    self.driver.find_element(By.XPATH, "//*[@id='read-job-accountid']").send_keys("1234")
    self.driver.find_element(By.XPATH, "//button[@class='btn btn-success save-button']").click()
    self.waitForClickable("//*[@id='edit-job-number']")
    self.driver.find_element(By.ID, "edit-job-number").send_keys("777")
    self.waitForClickable("//*[@id='edit-start-date']")
    self.driver.find_element(By.ID, "edit-start-date").send_keys("11/23/2000")
    self.waitForClickable("//*[@id='edit-end-date']")
    self.driver.find_element(By.ID, "edit-end-date").send_keys("11/24/2000")
    self.waitForClickable("//*[@id='edit-billable']")
    self.driver.find_element(By.XPATH, '//*[@id="edit-billable"]/select/option[1]').click()
    self.waitForClickable('//*[@id="edit-status"]/select')
    self.driver.find_element(By.XPATH, '//*[@id="edit-status"]/select/option[2]').click()
    self.driver.implicitly_wait(1)
    #confirm success message
    self.driver.find_element(By.XPATH, '//*[contains(.,"successfully saved")]//*[@class="alert alert-success ng-binding"]')
    

  def delete(self):
    self.goToJobList()
    time.sleep(1)
    self.waitForClickable("//tr[contains(.,'Projecttest')]//a[contains(@href,'Job')]")
    self.waitForClickable("//button[@class='btn btn-default dropdown-toggle']")
    self.waitForClickable("//a[contains(.,'Delete')]")
    self.driver.find_element(By.XPATH, "//button[contains(.,'Delete')]").click()
    #confirm success message
    self.driver.find_element(By.XPATH, '//*[@id="ext-gen125"]')


  def test_job_crud(self):
    self.login(email,password)
    self.goToJobList()
    self.create()
    self.driver.implicitly_wait(2)
    self.update()
    time.sleep(1)
    self.delete()
    self.driver.implicitly_wait(1)
    


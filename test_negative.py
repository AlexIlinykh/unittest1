import pytest
import time
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.alert import Alert

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

  def clearJobName(self):
    self.driver.find_element(By.ID, "edit-job-name").click()
    self.driver.find_element(By.ID, "edit-job-name").clear()

  def editJob(self):
    self.driver.find_element(By.XPATH, "//tr[contains(.,'Sample Project1')]//a[contains(@href,'Job')]").click() #pass string
    self.waitForClickable("//button[@id='BasicInfoTemplate-btn-edit']")
    self.waitForClickable("//*[@id='read-job-accountid']")

  def login(self, email, password):
    self.driver.get("https://login.clicktime.com")
    self.driver.find_element(By.ID, "email").click()
    self.driver.find_element(By.ID, "email").send_keys(email)
    self.driver.find_element(By.ID, "password").click()
    self.driver.find_element(By.ID, "password").send_keys(password)
    self.driver.find_element(By.ID, "loginbutton").click()
    self.driver.find_element(By.ID, "username")

  def createfail(self):
    alert = Alert(self.driver)
    self.driver.get('https://app.clicktime.com/App/Details/Job/#/entityDetail')
    self.driver.implicitly_wait(1)
    self.driver.find_element(By.ID, "edit-job-client").click()
    self.driver.find_element(By.ID, "ui-select-choices-row-0-0").click()  #choose by client name and make client name a variable
    self.driver.find_element(By.ID, "edit-job-name").click()
    self.driver.find_element(By.ID, "edit-job-name").send_keys("Projecttest") #capture time stamp and use variable for project name
    self.driver.find_element(By.CLASS_NAME, "btn-success").click()
    #confirm error message
    time.sleep(1)
    self.driver.find_element(By.ID, "JobNumberErrorRequire")
    self.goToJobList()
    alert.accept()

  def updatefail(self):
      alert = Alert(self.driver)
      self.goToJobList()
      self.editJob()
      #update all properties
      self.clearJobName()
      time.sleep(1)
      #confirm error message
      self.driver.find_element(By.ID, "JobNumberErrorRequire")
      self.goToJobList()
      alert.accept()

  def updatefaildate(self):
    alert = Alert(self.driver)
    self.editJob()
    
    self.driver.find_element(By.ID, "edit-job-name").click()
    self.driver.find_element(By.ID, "edit-job-name").send_keys("name")

    self.waitForClickable("//*[@id='edit-job-number']")
    self.driver.find_element(By.ID, "edit-job-number").send_keys("777")

    self.waitForClickable("//*[@id='edit-start-date']")
    self.driver.find_element(By.ID, "edit-start-date").send_keys("62353")
    #confirm fail message
    self.driver.find_element(By.XPATH, "//span[contains(.,'Start date must be a')]")
    self.goToJobList()
    alert.accept()
    time.sleep(1)

  def test_job_crud(self):
    self.login(email,password)
    self.goToJobList()
    self.createfail()
    self.updatefail()
    self.updatefaildate()
    

    
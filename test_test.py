
import pytest
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By

f = open("login.txt", "r")
lines = f.readlines()
f.close()
email = lines[0].strip('\n')
password = lines[1]
class Test(unittest.TestCase):
  @classmethod
  def setUpClass(self):
    self.driver = webdriver.Chrome()
    self.vars = {}
  @classmethod
  def tearDownClass(self):
    self.driver.quit()

  
  def login(self, email, password):
    self.driver.get("https://login.clicktime.com")
    self.driver.find_element(By.ID, "email").click()
    self.driver.find_element(By.ID, "email").send_keys(email)
    self.driver.find_element(By.ID, "password").click()
    self.driver.find_element(By.ID, "password").send_keys(password)
    self.driver.find_element(By.ID, "loginbutton").click()


  def test_pass(self):
    self.login(email,password)
    self.driver.find_element(By.ID, "username")
  

  def test_fail_password(self):
    self.login(email,"incorrect")
    self.driver.find_element(By.ID, "signinAlert")

  def test_fail_username(self):
    self.login("incorrect@gmail.com",password)
    self.driver.find_element(By.ID, "signinAlert")

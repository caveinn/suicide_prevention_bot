import time
import pickle
import numpy as np
import os

from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from sklearn.feature_extraction.text import HashingVectorizer
from usefulMethods import vect

driver = webdriver.Chrome("./chromedriver-linux64/chromedriver")


def login():
  driver.get("http://www.twitter.com/login")
  time.sleep(5)
  if not("log in" in driver.title.lower()):
    print(driver.title)
    print("login" in driver.title)
    return
  usernameInput = driver.find_element_by_tag_name("input")
  usernameInput.clear()
  usernameInput.send_keys(os.getenv("TWITTER_NUMBER"))
  usernameInput.send_keys(Keys.ENTER)
  time.sleep(2) 
  passwordOrNameInput = driver.find_elements_by_tag_name("input")
  if len(passwordOrNameInput) == 1:
        passwordOrNameInput[0].clear()
        passwordOrNameInput[0].send_keys(os.getenv("TWITTER_USER_NAME"))
        passwordOrNameInput[0].send_keys(Keys.ENTER)
        time.sleep(2)
        passwordOrNameInput = driver.find_elements_by_tag_name("input")
 
  passwordInput =  passwordOrNameInput[1]
  passwordInput.send_keys(os.getenv("TWITTER_PASSWORD"))
  passwordInput.send_keys(Keys.ENTER)
  breakpoint()

login()
time.sleep(5)
visitedTweets = []

while True:
  tweetsInFeed = driver.find_elements_by_css_selector("[data-testid='tweet']")

  for tweet in tweetsInFeed:
    tweetTextDisp=""
    try:
      tweetTextDisp = tweet.find_element_by_css_selector('[lang="en"][dir="auto"]')
    except:
      continue
    print(tweetTextDisp.text)
    clf = ''
    with open("classifier.pickle", 'rb') as f:
        clf = pickle.load(f)

    label = {0: 'negative', 1: 'positive'}
    transformedText = vect.transform([tweetTextDisp.text])
    prediction = label[clf.predict(transformedText)[0]]
    probability = np.max(clf.predict_proba(transformedText))*100
    print('Prediction: %s\nProbability: %.2f%%' %
          (prediction, probability))

    if(prediction == label[1] and probability > 80 and not tweetTextDisp.text in visitedTweets ): # if tweet is predicted as suicidal reply to it
      visitedTweets.append(tweetTextDisp.text)
      commentBtn = tweet.find_elements_by_css_selector("svg")[1]
      commentBtn.click()
      commentTextArea = driver.find_element_by_css_selector("[data-testid='tweetTextarea_0']")
      commentTextArea.send_keys(" If you or someone you know is contemplating suicide, please do not hesitate to talk to someone Kenya Hotline: +254 722 178 177")
      commentSbmtBtn = driver.find_element_by_css_selector('[data-testid="tweetButton"]')
      commentSbmtBtn.click()

  time.sleep(10)
  driver.refresh()

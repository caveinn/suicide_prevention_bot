import time
import pickle
import numpy as np
import os

from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from sklearn.feature_extraction.text import HashingVectorizer
from usefulMethods import vect

driver = webdriver.Chrome()


def login():
  driver.get("http://www.twitter.com/login")
  time.sleep(5)
  if not("login" in driver.title.lower()):
    print(driver.title)
    print("login" in driver.title)
    return
  print(os.getenv("TWITTER_NUMBER"))
  usernameInput = driver.find_element_by_name("session[username_or_email]")
  usernameInput.clear()
  usernameInput.send_keys(os.getenv("TWITTER_NUMBER"))
  passwordInput = driver.find_element_by_name("session[password]")
  passwordInput.send_keys(os.getenv("TWITTER_PASSWORD"))
  passwordInput.send_keys(Keys.ENTER)

login()
time.sleep(5)
visitedTweets = []

while True:
  # login()
  # time.sleep(5)
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

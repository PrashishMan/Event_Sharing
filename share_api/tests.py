from selenium import webdriver
browser = webdriver.Firefox()

#User Story
#User navigtes to the home page
browser.get('http://localhost:3001/home')

#Browser redirects to the login page in not logged in

browser.quit()

assert 'Django' in browser.title

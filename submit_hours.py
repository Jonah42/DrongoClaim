import requests
import time
from requests_html import HTMLSession
from selenium import webdriver
from selenium.webdriver.common.by import By

translateDuty = {
	'Lab Demo': 'Lab demo',
	'Assessment': 'Assessment marking (online/paper-based)',
	'Exam': 'Exam marking (mid-term/final)',
	'Training': 'Training (School/Faculty/Course meeting)',
	'Tutoring': 'Tutoring',
	'Invigilation': 'Invigilation (Online/in-person for Exam/Assessment)',
	'Other': 'Other Duty'
}

def submit(data):
	options = webdriver.ChromeOptions()
	options.add_argument('user-data-dir=./User')
	browser=webdriver.Chrome('./chromedriver', options=options)
	browser.get('https://forms.office.com/Pages/ResponsePage.aspx?id=pM_2PxXn20i44Qhnufn7o8ltiXjgwdBMqx5Dt3_E2eBUODMwMzdDV0NTUlgzUkdHS0w5UkdEMVU5My4u')
	for course in reversed(data['courses']):
		while (len(browser.find_elements_by_css_selector('input')) != 3):
			try:
				backButton = browser.find_element_by_xpath("//button[@aria-label='Back']")
				backButton.click()
				time.sleep(1)
			except:
				time.sleep(1)
		submitCourse(browser, data['zid'], data['firstName'], data['lastName'], course)
	# Quit browser
	browser.quit()

def submitCourse(browser, zid, firstName, lastName, course):
	for slot in reversed(course['slots']):
		textInputs = {
			'Student/Staff ID (do not put Z in front of your ID):': zid[1:],
			'Surname:': lastName,
			'Given names:': firstName,
			'Date Worked : (input date in the format of dd/mm/yyyy )': f'{slot["date"]}/{slot["month"]}/2021'
		}
		mins = round(abs(int(slot["endMin"])-int(slot["startMin"]))*25/15)
		dropdownInputs = {
			'Course Code : (if you cannot find course code from the list, click "Other" to type in)': course['code'],
			'Start time:': f'{slot["startHour"]}:{slot["startMin"]}',
			'End time:': f'{slot["endHour"]}:{slot["endMin"]}',
			'Number of hours in this claim': f'{int(slot["endHour"])-int(slot["startHour"]) + (-1 if int(slot["endMin"])<int(slot["startMin"]) else 0)}' + ('' if slot["endMin"]==slot["startMin"] else f'.{mins if mins != 50 else 5}'),
			'Description of duty/task/job': translateDuty[slot['duty']],
			'Name of the lecturer/course coordinator/supervisor in charge ?': course['lecturer']
		}

		textAreaInputs = {
			'You may provide more info in this box about the task you have done especially if you did "Other Duty" in the Description of duty/task/job:': slot['note']
		}
		# Find all questions on current page
		questions = browser.find_elements_by_class_name('office-form-question-content')
		for question in questions:
			# Get all spans and see if one of them fits
			spans = question.find_elements(By.CSS_SELECTOR, 'span')
			for span in spans:
				text = span.text
				if text in textInputs:
					inputField = question.find_element(By.CSS_SELECTOR, 'input')
					inputField.clear()
					inputField.send_keys(textInputs[text])
					break
			else:
				raise Exception('Could not find appropriate question')
		# Progress to next page
		button = browser.find_element_by_xpath("//button[@aria-label='Next']")
		button.click()
		# Find all questions on the current page
		questions = browser.find_elements_by_class_name('office-form-question-content')
		for question in questions:
			# Get all spans and see if one of them fits
			spans = question.find_elements(By.CSS_SELECTOR, 'span')
			for span in spans:
				text = span.text
				if text in textInputs:
					inputField = question.find_element(By.CSS_SELECTOR, 'input')
					inputField.clear()
					inputField.send_keys(textInputs[text])
					break
				elif text in textAreaInputs:
					inputField = question.find_element(By.CSS_SELECTOR, 'textarea')
					inputField.clear()
					inputField.send_keys(textAreaInputs[text])
					break
				elif text in dropdownInputs:
					question.find_element(By.CSS_SELECTOR, 'i').click()
					innerSpans = question.find_elements(By.CSS_SELECTOR, 'span')
					for innerSpan in innerSpans:
						if innerSpan.text == dropdownInputs[text]:
							innerSpan.click()
							break
					else:
						raise Exception(f'Could not find dropdown {dropdownInputs[text]} for question {text}')
					break
			else:
				raise Exception('Could not find appropriate question')
		# Request an email receipt
		checkbox = browser.find_element_by_class_name('checkbox')
		if checkbox.find_element(By.CSS_SELECTOR, 'span').text == 'Send me an email receipt of my responses':
			checkbox.find_element(By.CSS_SELECTOR, 'input').click()
		else:
			raise Exception('Could not find receipt checkbox')
		# Submit form (UNCOMMENT TO SUBMIT)
		browser.find_element(By.CLASS_NAME, '__submit-button__').click()
		# Return to the start of the form
		while (len(browser.find_elements(By.CSS_SELECTOR, 'a')) != 5):
			# print(len(browser.find_elements(By.CSS_SELECTOR, 'a')))
			time.sleep(1)
		links = browser.find_elements(By.CSS_SELECTOR, 'a')
		for link in links:
			# print(link.text)
			if link.text == 'Submit another response':
				link.click()
				break
		else:
			raise Exception('Could not find link back to start of form')

# if __name__ == "__main__":
# 	main()
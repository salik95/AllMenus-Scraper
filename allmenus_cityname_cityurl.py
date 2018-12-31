import csv
from selenium import webdriver

driver = webdriver.Chrome()
driver.get('https://www.allmenus.com/')

state_links = []

column_names = ['City Name', 'City URL']

links = driver.find_elements_by_css_selector('ul.state-list li a')
for link in links:
	state_links.append([link.text, link.get_attribute('href')])

for sl in state_links:
	data_city_links = []
	driver.get(sl[1])
	cities = driver.find_elements_by_css_selector('div.cities-column a')
	for city in cities:
		if city.get_attribute('href') == 'https://www.allmenus.com/al/':
			break
		data_city_links.append([city.text, city.get_attribute('href')])
	outfile = open(sl[0] + '.csv', 'w')
	outcsv = csv.writer(outfile)
	outcsv.writerow([column for column in column_names])
	[outcsv.writerow([value for value in item]) for item in data_city_links]
	outfile.close()
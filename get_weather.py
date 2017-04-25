# -*- coding:utf8 -*-

from bs4 import BeautifulSoup as bs
import requests
import re


tokyo_url = 'http://www.jma.go.jp/jp/yoho/319.html'
okinawa_url = 'http://www.jma.go.jp/jp/yoho/353.html'


def get():
	for area, url in {'東京': tokyo_url, '沖縄': okinawa_url}.items():
		print(area + ':')
		html_resource = requests.get(url)
		obj_resource = bs(html_resource.text, 'lxml')
		tr_list = obj_resource.find('table', {'id': 'forecasttablefont'}).findAll('tr', recursive=False)

		if len(tr_list) <= 0:
			return False

		# (0番目からスタート)１番目から3番目が天気
		# 1 -> 今日, 2 -> 明日, 3 -> 明後日の天気

		for i in range(1, 4):
			# 天気
			weather_section = tr_list[i].find('th', {'class': 'weather'})
			weather_title = weather_section.find('img')['title']

			# 天気情報
			info_section = tr_list[i].find('td', {'class': 'info'})
			# brを消すかな？
			info = re.sub('\s', '', info_section.get_text())

			# 降水確率
			rainy_section = tr_list[i].find('td', {'class': 'rain'})
			rainy_tr_list = rainy_section.findAll('tr')
			rainy_list = []
			for rainy_tr in rainy_tr_list:
				_left = rainy_tr.find('td', {'align': 'left'}).string if rainy_tr.find('td', {'align': 'left'}) is not None else ''
				_right = rainy_tr.find('td', {'align': 'right'}).string if rainy_tr.find('td', {'align': 'right'}) is not None else ''
				rainy_list.append(_left + ' ' + _right)

			# 気温予報
			temp_section = tr_list[i].find('td', {'class': 'temp'})
			temp_tr_list = temp_section.findAll('tr')
			# 1番目から
			temp_string = ''
			if 1 in temp_tr_list:
				temp_tr = temp_tr_list[1]
				temp_city = temp_tr.find('td', {'class': 'city'}).string
				temp_min = temp_tr.find('td', {'class': 'min'}).string
				temp_max = temp_tr.find('td', {'class': 'max'}).string
				temp_string = temp_city + ':' + temp_max

			print(weather_title)
			print(info)
			print(', '.join(rainy_list))
			print(temp_string)

	return True


def main():
	result = get()


if __name__ == '__main__':
	main()

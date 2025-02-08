from transliterate import translit
import requests as rq

# Правило модуля - выход каждой функции только True или False

def check_by_name(mas, current_name):
	required_name = mas[0]
	bool_otklonenie = mas[1]
	if required_name == '':
		return True

	st1 = (translit(current_name, 'ru') == required_name) # из en в ru
	st2 = (translit(required_name, 'ru', reversed=True) == current_name) # из ru в en
	st3 = (required_name == current_name)
	if bool_otklonenie == False:
		if st1 or st2 or st3:
			return True
		return False

	if st1 or st2 or st3:
		return True

	return False

def check_by_surname(mas, current_surname):
	required_surname = mas[0]
	bool_otklonenie = mas[1]
	if required_surname == '':
		return True

	st1 = (translit(current_surname, 'ru') == required_surname) # из en в ru
	st2 = (translit(required_surname, 'ru', reversed=True) == current_surname) # из ru в en
	st3 = (required_surname == current_surname)
	if bool_otklonenie == False:
		if st1 or st2 or st3:
			return True
		return False

	if st1 or st2 or st3:
		return True

	return False


def check_by_sex(mas, current_sex):
	required_sex = mas[0]
	bool_otklonenie = mas[1]
	if required_sex == 'Не определено':
		return True
	if bool_otklonenie == True: # можно же поставить какой угодно, так что отклонение указывает, что нет смысла проверять
		return True

	if required_sex == current_sex:
		return True
	return False

def check_by_bdate(mas, current_bdate):
	required_bdate = mas[0]
	bool_otklonenie = mas[1]

	if required_bdate == '':
		return True
	if required_bdate == current_bdate:
		return True
	return False


def check_by_city(mas, current_city):
	required_city = mas[0]
	bool_otklonenie = mas[1]

	if required_city == '':
		return True

	st1 = (translit(current_city, 'ru') == required_city) # из en в ru
	st2 = (translit(required_city, 'ru', reversed=True) == current_city) # из ru в en
	st3 = (required_city == current_city)

	if bool_otklonenie == False:
		if st1 or st2 or st3:
			return True
		return False

	if st1 or st2 or st3:
		return True
	return False

def check_by_relatives(mas, current_relatives): # на вход 2 списка, полное или неполное совпадение сделать
	required_relatives = mas[0]
	bool_otklonenie = mas[1]
	if current_relatives == [] or current_relatives == None:
		return True

	for rr in required_relatives:
		for cr in current_relatives:
			if rr == cr and bool_otklonenie == True:
				return True
			if rr != cr and bool_otklonenie == False:
				return False

	return True

def check_by_relation(mas, current_relation, cur_sex, partner_sex):
	required_relation = mas[0]
	bool_otklonenie = mas[1]
	if required_relation == 'Не определено':
		return True

	if required_relation == current_relation:
		return True

	if bool_otklonenie == True:
		if partner_sex == None or cur_sex == None:
			return False
		if partner_sex == 0 or cur_sex == 0:
			return True
		if partner_sex == cur_sex:
			return True
	return False

def check_by_can_write_private_messages(required_cwpm_state, current_cwpm_state):
	if required_cwpm_state == 'Не определено':
		return True
	if required_cwpm_state == current_cwpm_state:
		return True
	return False

if __name__ == '__main__':
	text = 'abobius'
	ru_text = translit(text, 'ru')

from kivy.config import Config
Config.set("graphics", "resizable", 0)
Config.set("graphics", "width", 800)
Config.set("graphics", "height", 500)
import string
import con_and_fill_database as cafd
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
import random
from kivy.uix.textinput import TextInput

from kivy.uix.dropdown import DropDown
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.checkbox import CheckBox
from kivy.clock import Clock
from kivy.uix.popup import Popup
import json

import threading
import queue
import pyperclip
dict_rel = {'1 - не женат/не замужем;' : 1,
'2 — есть друг/есть подруга' : 2,
'3 — помолвлен/помолвлена' : 3,
'4 — женат/замужем' : 4,
'5 — всё сложно' : 5,
'6 — в активном поиске' : 6,
'7 — влюблён/влюблена' : 7,
'8 — в гражданском браке' : 8,
'0 — не указано': 0,
'Не определено':'Не определено'}

dict_sex = {'1 — женский': 1, 
			'2 — мужской': 2,
			'0 — пол не указан':0,
			 'Не определено':'Не определено'}

dict_cwpm = {'1 - можно': 1,
			 '0 - нельзя': 0,
			 'Не определено':'Не определено'}

class MainApp(App):
	def on_enter(instance, value):
		print('user pressed enter in', instance)

	def on_checkbox_active(self, checkbox, value):
	    if value:
	        print('The checkbox', checkbox, 'is active')
	    else:
	        print('The checkbox', checkbox, 'is inactive')

	def creating_first_window(self):
		first_window = Screen(name = 'first')
		# устанавливаем сетку
		layout = GridLayout(cols = 3,
							rows = 15,
							spacing = [10, 10],
							row_force_default = True,
							row_default_height = 40)
		first_window.add_widget(layout)
		
		# Блок верхних подписей. Нулевая строка. Начало
		opisanie_label_0 = Label(text = 'Характеристика')
		opisanie_label_1 = Label(text = 'Значение')
		opisanie_label_2 = Label(text = 'Включить обработку отклонений')

		layout.add_widget(opisanie_label_0)
		layout.add_widget(opisanie_label_1)
		layout.add_widget(opisanie_label_2)
		# Блок верхних подписей. Нулевая строка. Конец

		# Блок первой строки. Начало
		self.label_stroka_1 = Label(text = 'Имя:')
		self.textinput_stroka_1 = TextInput( hint_text = 'Не определено',
										multiline = False)
		self.checkbox_stroka_1 = CheckBox()

		layout.add_widget(self.label_stroka_1)
		layout.add_widget(self.textinput_stroka_1)
		layout.add_widget(self.checkbox_stroka_1)
		# Блок первой строки. Конец

		# Блок второй строки. Начало
		self.label_stroka_2 = Label(text = 'Фамилия:')
		self.textinput_stroka_2 = TextInput(hint_text = 'Не определено',
								multiline = False)
		self.checkbox_stroka_2 = CheckBox()

		layout.add_widget(self.label_stroka_2)
		layout.add_widget(self.textinput_stroka_2)
		layout.add_widget(self.checkbox_stroka_2)

		# Блок второй строки. Конец

		# Блок третьей строки. Начало
		self.label_stroka_3 = Label(text = 'Пол:')
		dropdown_stroka_3 = DropDown()
		for sex in dict_sex.keys():
			btn = Button(text = sex, size_hint_y=None, height=30)
			btn.bind(on_release=lambda btn: dropdown_stroka_3.select(btn.text))
			dropdown_stroka_3.add_widget(btn)

		self.but_call_drop_stroka_3 = Button(text='Не определено')
		self.but_call_drop_stroka_3.bind(on_release=dropdown_stroka_3.open)
		dropdown_stroka_3.bind( on_select=lambda instance, 
								x: setattr(self.but_call_drop_stroka_3, 'text', x))
		self.checkbox_stroka_3 = CheckBox()

		layout.add_widget(self.label_stroka_3)
		layout.add_widget(self.but_call_drop_stroka_3)
		layout.add_widget(self.checkbox_stroka_3)
		# Блок третьей строки. Конец

		# Блок четвертой строки. Начало
		self.label_stroka_4 = Label(text = "Дата рождения/возраст")
		self.textinput_stroka_4 = TextInput( hint_text = 'Не определено',
										multiline = False)
		self.checkbox_stroka_4 = CheckBox()

		layout.add_widget(self.label_stroka_4)
		layout.add_widget(self.textinput_stroka_4)
		layout.add_widget(self.checkbox_stroka_4)
		# Блок четвертой строки. Конец

		# Блок пятой строки. Начало
		self.label_stroka_5 = Label(text = 'Город:')
		self.textinput_stroka_5 = TextInput( hint_text = 'Не определено',
										multiline = False)
		self.checkbox_stroka_5 = CheckBox()

		layout.add_widget(self.label_stroka_5)
		layout.add_widget(self.textinput_stroka_5)
		layout.add_widget(self.checkbox_stroka_5)
		# Блок пятой строки. Конец

		# Блок шестой строки. Начало
		self.label_stroka_6 = Label(text = 'Родственники (id, через запятую):')
		self.textinput_stroka_6 = TextInput( hint_text = 'Не определено',
										multiline = False)
		self.checkbox_stroka_6 = CheckBox()

		layout.add_widget(self.label_stroka_6)
		layout.add_widget(self.textinput_stroka_6)
		layout.add_widget(self.checkbox_stroka_6)
		# Блок шестой строки. Конец

		# Блок седьмой строки. Начало
		self.label_stroka_7 = Label(text = 'Семейное положение:')
		dropdown_stroka_7 = DropDown()
		for rel in dict_rel.keys():
			btn = Button(	text = rel, 
							size_hint_y = None, 
							height = 30)
			btn.bind(on_release=lambda btn: dropdown_stroka_7.select(btn.text))
			dropdown_stroka_7.add_widget(btn)

		self.but_call_drop_stroka_7 = Button(text='Не определено')
		self.but_call_drop_stroka_7.bind(on_release=dropdown_stroka_7.open)
		dropdown_stroka_7.bind(	on_select=lambda instance, 
									x: setattr(self.but_call_drop_stroka_7, 'text', x))

		self.checkbox_stroka_7 = CheckBox()
		layout.add_widget(self.label_stroka_7)
		layout.add_widget(self.but_call_drop_stroka_7)
		layout.add_widget(self.checkbox_stroka_7)
		# Блок седьмой строки. Конец


		# Блок восьмой строки. Начало
		self.label_stroka_8 = Label(text = 'Можно ли писать сообщения')
		
		dropdown_stroka_8 = DropDown()

		#dict_cwpm
		for cwpm in dict_cwpm.keys():
			bufbtn1 = Button(	text = cwpm, 
								size_hint_y=None, 
								height=30)
			bufbtn1.bind(on_release=lambda bufbtn1: dropdown_stroka_8.select(bufbtn1.text))
			dropdown_stroka_8.add_widget(bufbtn1)

		self.but_call_drop_stroka_8 = Button(text = 'Не определено')
		self.but_call_drop_stroka_8.bind(on_release=dropdown_stroka_8.open)
		dropdown_stroka_8.bind( on_select = lambda instance, 
								x: setattr(self.but_call_drop_stroka_8, 'text', x))

		layout.add_widget(self.label_stroka_8)
		layout.add_widget(self.but_call_drop_stroka_8)
		# Блок восьмой строки. Конец

		bufbtn1 = Button(text='Продолжить', size_hint_y=None, height=30)
		bufbtn1.bind(on_release = self.change)
		layout.add_widget(bufbtn1)
		return first_window

	def creating_second_window(self):
		second_window = Screen(name = 'second')

		layout = GridLayout(cols = 2,
							rows = 4,
							row_force_default = True, # включить статический размер
							# для строк 
							row_default_height = 60, # высота по умолчанию
							#col_force_default = True, # включить стат.размер для коллон
							#col_default_width = 40
							)
		second_window.add_widget(layout)
		page_2_label_stroka_0 = Label(text = 'Ссылка/id/короткое_имя')
		self.page_2_textinput_stroka_0 = TextInput(	hint_text = 'Введите ссылку/id/короткое_имя',
												multiline = False)
		page_2_label_stroka_1 = Label(text = 'Введите степень поиска')
		self.page_2_textinput_stroka_1 = TextInput(	hint_text = '1-3',
												multiline = False)

		layout.add_widget(page_2_label_stroka_0)
		layout.add_widget(self.page_2_textinput_stroka_0)
		layout.add_widget(page_2_label_stroka_1)
		layout.add_widget(self.page_2_textinput_stroka_1)
		layout.add_widget(Button(text = "Вернуться назад", 
				on_release = self.change))
		layout.add_widget(Button(text = "Запустить поиск", 
				on_release = self.launch))
		return second_window

	def creating_third_window(self):
		third_window = Screen(name = 'third')
		self.label_page3 = Label(text = '0 %')
		third_window.add_widget(self.label_page3)
		
		return third_window
	def creating_fourth_window(self):
		fourth_window = Screen(name = 'fourth')

		layout = GridLayout(cols = 2,
							rows = 8,
							row_force_default = True,
							row_default_height = 60)
		fourth_window.add_widget(layout)
		# self.id_first = 1
		# self.max_ln = cafd.take_len()
		but1 = Button(text='<')
		but2 = Button(text='>')
		but1.bind(on_release = self.decrease_page)
		but2.bind(on_release = self.increase_page)
		
		
		self.label_page4_row1 = Label(text = '')
		self.button_page4_row1 = Button(text = '')
		
		self.label_page4_row2 = Label(text = '')
		self.button_page4_row2 = Button(text = '')

		self.label_page4_row3 = Label(text = '')
		self.button_page4_row3 = Button(text = '')

		self.label_page4_row4 = Label(text = '')
		self.button_page4_row4 = Button(text = '')

		self.label_page4_row5 = Label(text = '')
		self.button_page4_row5 = Button(text = '')

		self.button_page4_row1.bind(on_release = self.copy_source)
		self.button_page4_row2.bind(on_release = self.copy_source)
		self.button_page4_row3.bind(on_release = self.copy_source)
		self.button_page4_row4.bind(on_release = self.copy_source)
		self.button_page4_row5.bind(on_release = self.copy_source)

		layout.add_widget(self.label_page4_row1)
		layout.add_widget(self.button_page4_row1)
		layout.add_widget(self.label_page4_row2)
		layout.add_widget(self.button_page4_row2)
		layout.add_widget(self.label_page4_row3)
		layout.add_widget(self.button_page4_row3)
		layout.add_widget(self.label_page4_row4)
		layout.add_widget(self.button_page4_row4)
		layout.add_widget(self.label_page4_row5)
		layout.add_widget(self.button_page4_row5)

		layout.add_widget(but1)
		layout.add_widget(but2)


		self.first_id = None
		self.last_id = 0
		

		return fourth_window

	def fill_rows(self, type):
		if type == 'next':
			mas, self.first_id, self.last_id = cafd.take_next_page(self.first_id, self.last_id)
		else:
			mas, self.first_id, self.last_id = cafd.take_prev_page(self.first_id, self.last_id)

		if mas == None:
			return

		while len(mas) < 5:
			mas.append(('', '', '', ''))
		self.button_page4_row1.text = str(mas[0][2])
		self.button_page4_row2.text = str(mas[1][2])
		self.button_page4_row3.text = str(mas[2][2])
		self.button_page4_row4.text = str(mas[3][2])
		self.button_page4_row5.text = str(mas[4][2])
		
	def increase_page(self, instance):
		self.fill_rows('next')
	def decrease_page(self, instance):
		self.fill_rows('prev')
			
	def copy_source(self, instance):
		pyperclip.copy('https://vk.com/id' + instance.text)


	def change_label_page_3(self, instance):
		while not self.q.empty():
			from_queue = self.q.get()
			if from_queue == '100%':
				Clock.unschedule(self.event)
				self.label_page3.text = 'Программа выполнена: 100%'
				self.root.current = 'fourth'
				self.fill_rows('next')
				return
			self.label_page3.text = f"Процент выполнения: {from_queue}"

	def build(self):
		windowmanager = ScreenManager()  
		windowmanager.add_widget(self.creating_first_window())
		windowmanager.add_widget(self.creating_second_window())
		windowmanager.add_widget(self.creating_third_window())
		windowmanager.add_widget(self.creating_fourth_window())
		return windowmanager

	def change(self, instance):
		if self.root.current == 'first':
			self.root.current = 'second'
			self.root.transition.direction = 'left'
		else:
			self.root.current = 'first'
			self.root.transition.direction = 'right'

	def launch(self, instance):
		self.root.current = 'third'
		self.root.transition.direction = 'left'

		stroka = self.textinput_stroka_6.text.replace(' ', '')
		output_mas = stroka.split(',')
		if len(output_mas) == 1 and output_mas[0] == '':
			output_mas = []
		
		try:
			output_mas = list(map(int, output_mas))
		except:
			screen_popup = Screen(name = 'popup')
			popup_layout = GridLayout(cols = 1,
					rows = 2,
					row_force_default = True,
					row_default_height = 60)
			screen_popup.add_widget(popup_layout)

			popup_layout.add_widget(Label(text='У вас где то ошибка пожалуйста перепроверьте че ввели'))
			content = Button(text='Закрыть оповещение')
			popup_layout.add_widget(content)

			popup = Popup(title='Возникла ошибочка', content=screen_popup, auto_dismiss=False)
			content.bind(on_press=popup.dismiss)
			popup.open()
			self.root.current = 'first'
			return

		to_json = {'first_name': [self.textinput_stroka_1.text[:100].strip(), self.checkbox_stroka_1.active],
		'last_name': [self.textinput_stroka_2.text[:100].strip(), self.checkbox_stroka_2.active],
		'sex': [dict_sex.get(self.but_call_drop_stroka_3.text), self.checkbox_stroka_3.active],
		'bdate': [self.textinput_stroka_4.text[:20].strip(), self.checkbox_stroka_4.active],
		'city': [self.textinput_stroka_5.text[:50].strip(), self.checkbox_stroka_5.active],
		'relatives': [output_mas, self.checkbox_stroka_6.active],
		'relation': [dict_rel.get(self.but_call_drop_stroka_7.text), self.checkbox_stroka_7.active],
		'can_write_private_message': [dict_cwpm.get(self.but_call_drop_stroka_8.text), None]}

		with open('from_gui.json', 'w', encoding='utf-8') as f:
			f.write(json.dumps(to_json,ensure_ascii=False))

		self.q = queue.Queue()
		
		self.event = Clock.schedule_interval(self.change_label_page_3, 1)
		self.thread = threading.Thread(target=cafd.launch_opredelenie, args=(self.page_2_textinput_stroka_0.text, int(self.page_2_textinput_stroka_1.text), self.q,), daemon=True)
		self.thread.start()


if __name__ == '__main__':
	MainApp().run()
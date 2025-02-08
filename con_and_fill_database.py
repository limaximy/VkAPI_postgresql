import psycopg2
DEFAULT_DATABASE_NAME = 'database_with_ids'
import request_to_vk as rtv
import matching_check as mc
import json
import time
def create_data_base():
	conn = psycopg2.connect(
	dbname="postgres",
	user="postgres",
	password="password",
	host="localhost",
	port="5432"
	)
	conn.autocommit = True
	with conn.cursor() as cur:
		cur.execute(f'CREATE DATABASE {DEFAULT_DATABASE_NAME};')
		conn.commit()
	return


def create_and_fill_table(first_id, stepen):
	with psycopg2.connect(
	dbname = DEFAULT_DATABASE_NAME,
	user = "postgres",
	password = "password",
	host = "localhost",
	port = "5432"
	) as conn:
		with conn.cursor() as cur:
			cur.execute('DROP TABLE IF EXISTS persons;')
			conn.commit()
			cur.execute('''
				CREATE TABLE IF NOT EXISTS persons (
					id SERIAL PRIMARY KEY,
					cur_number INTEGER,
					vk_id INTEGER,
					type_of_match INTEGER
				);
			''')
			conn.commit()
			list_for_obrabotka = [first_id]
			n = 0
			m = len(list_for_obrabotka)
			cur.execute('INSERT INTO persons (cur_number, vk_id) VALUES (%s, %s)', (0, list_for_obrabotka[0]))
			conn.commit()
			for i in range(stepen-1):
				bufm = m-1
				for nn in range(n, m):
					cur.execute('SELECT vk_id FROM persons where cur_number = %s' , (nn,))
					current_user_id = cur.fetchall()
					current_user_id = current_user_id[0][0]
					list_for_obrabotka = rtv.take_friendlist_from_person_id(current_user_id)
					
					for friend in list_for_obrabotka:
						bufm +=1
						cur.execute('INSERT INTO persons (cur_number, vk_id) VALUES (%s, %s)', (bufm, friend))
						conn.commit()
				n = m+1
				m += bufm


def matching_search(queue):
	with psycopg2.connect(
	dbname = DEFAULT_DATABASE_NAME,
	user = "postgres",
	password = "password",
	host = "localhost",
	port = "5432"
	) as conn:
		with conn.cursor() as cur:
			cur.execute('SELECT vk_id FROM persons')
			dlina = len(cur.fetchall())
			with open('from_gui.json', 'r', encoding='utf-8') as f:
				json_required = json.load(f)

			cur.execute('SELECT vk_id FROM persons')
			count = 0
			for i in cur.fetchall():
				s = rtv.request_to_all_profile_info(i)
				if s == []:
					print('Успешный запрос, но страница не найдена')
					continue

				check_first_name = True
				check_last_name = True
				check_sex = True
				check_bdate = True
				check_city = True
				check_relatives = True
				check_relation = True
				check_cwpm = True
				check_first_name = mc.check_by_name(json_required.get('first_name'), s.get('first_name')) 
				check_last_name = mc.check_by_surname(json_required.get('last_name'), s.get('last_name'))

				if s.get('sex') != None:
					check_sex = mc.check_by_sex(json_required.get('sex'), s.get('sex'))
				if s.get('bdate') != None:
					check_bdate = mc.check_by_bdate(json_required.get('bdate'), s.get('bdate'))
				if s.get('city') != None:
					check_city = mc.check_by_city(json_required.get('city'), s.get('city').get('title'))
				if s.get('relatives') != [] and s.get('relatives') != None:
					mas_relatives = []
					for buf in s.get('relatives'):
						if buf.get('id') > 0:
							mas_relatives.append(buf.get('id'))
					check_relatives = mc.check_by_relatives(json_required.get('relatives'), mas_relatives)
				if s.get('relation') != None:
					partner_sex = None
					if json_required.get('relation')[1] == True:
						if s.get('relation_partner') != None:
							buf = rtv.request_to_all_profile_info(s.get('relation_partner').get('id'))
							if buf == []:
								print('Успешный запрос, но страница не найдена')
							else:
								partner_sex = buf.get('sex')

					check_relation = mc.check_by_relation(json_required.get('relation'), s.get('relation'), s.get('sex'), partner_sex)
				if s.get('can_write_private_message') != None:
					check_cwpm = mc.check_by_can_write_private_messages(json_required.get('can_write_private_message')[0], s.get('can_write_private_message'))
				
				if (check_first_name and check_last_name and check_sex and check_bdate and check_city and check_relatives and check_relation and check_cwpm) == False:
					cur.execute(f"UPDATE persons SET type_of_match = 0 WHERE cur_number = {count}")
					conn.commit()
				else:
					cur.execute(f"UPDATE persons SET type_of_match = 1 WHERE cur_number = {count}")
					conn.commit()
				count += 1
				if queue != None:
					queue.put(str(int(count/dlina*100)) +'%')
			if queue != None:
				queue.put("100%")
			
def take_next_page(first_id, last_id):
	with psycopg2.connect(
	dbname = DEFAULT_DATABASE_NAME,
	user = "postgres",
	password = "password",
	host = "localhost",
	port = "5432"
	) as conn:
		with conn.cursor() as cur:
			cur.execute('''SELECT * FROM persons
						WHERE type_of_match = 1 AND id > %s
						ORDER BY id
						LIMIT 5''', (last_id, ) )
			rows = cur.fetchall()

			if rows:
				first_id = rows[0][0]
				last_id = rows[-1][0]
				return rows, first_id, last_id
			return None, first_id, last_id

def take_prev_page(first_id, last_id):
	if first_id == None:
		return None. first_id, last_id

	with psycopg2.connect(
	dbname = DEFAULT_DATABASE_NAME,
	user = "postgres",
	password = "password",
	host = "localhost",
	port = "5432"
	) as conn:
		with conn.cursor() as cur:
			cur.execute('''SELECT * FROM persons
						WHERE type_of_match = 1 AND id < %s
						ORDER BY id
						DESC LIMIT 5''', (first_id, ) )
			rows = cur.fetchall()
			if rows:
				first_id = rows[-1][0]
				last_id = rows[0][0]
				return rows[::-1], first_id, last_id
			return None, first_id, last_id


def launch_opredelenie(vk_name, level, queue):
	try:
		create_data_base()
	except:
		print('База данных уже существует')
	create_and_fill_table(rtv.id_from_screen_name(vk_name), level) # 1 - токо пользователь, 3 - друзья друзей
	matching_search(queue)



if __name__ == '__main__':
	print(take_results_from_to(10))

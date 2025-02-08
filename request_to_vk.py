import requests as rq
import time

version = 5.199
token = 'put_ur_token_here'

def request_to_all_profile_info(owner_id):
    time.sleep(0.5)
    source_metod = "https://api.vk.com/method/users.get"
    rp = rq.get(source_metod,
                        params = {
                            'access_token':token,
                            'v':version,
                            'user_ids': owner_id,
                            'fields': 'bdate, can_write_private_message, city, relation, relatives, sex'
                        })
    rp = rp.json()
    error = rp.get('error')
    if error != None:
        print(error.get('error_msg'))
        return []
    s = rp.get('response')
    if s == []:
        return []

    return s[0]

def id_from_screen_name(screen_name):
    time.sleep(0.5)
    source_metod = "https://api.vk.com/method/users.get"
    response = rq.get(source_metod,
                        params = {
                            'access_token':token,
                            'v':version,
                            'user_ids': screen_name
                        })

    return response.json().get('response')[0].get('id')

def request_to_friend_list(main_person_id):
    source_metod = "https://api.vk.com/method/friends.get"
    response = rq.get(source_metod,
                    params = {
                        'access_token':token,
                        'v':version,
                        'user_id': main_person_id,
                        'fields': 'lists'
                    })
    return response

def take_friendlist_from_person_id(person_id):
    current_id = id_from_screen_name(person_id)
    rp = request_to_friend_list(current_id)

    try:
        list_of_friends = rp.json().get('response').get('items')
        list_of_ids = []
        for idd in list_of_friends:
            list_of_ids.append(idd.get('id'))
        return list_of_ids
    except:
        return []
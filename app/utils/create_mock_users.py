from app import db
import urllib
import json
import random

def create_mock_users(num_users):
    data = urllib.request.urlopen(f'https://api.namnapi.se/v2/names.json?limit={num_users}').read()
    data = json.loads(data)
    def random_with_N_digits(n):
        range_start = 10**(n-1)
        range_end = (10**n)-1
        return random.randint(range_start, range_end)

    for i in data['names']:
        rand_mail = ''.join(random.choice("abcdefghijklmnopqrstyv") for _ in range(6))
        # rand_phone = f'070{random_with_N_digits(7)}'
        r_email = rand_mail + "@kaffesump.se"
        r_first_name = i['firstname']
        r_last_name = i['surname']
        r_phone_number = f'070{random_with_N_digits(7)}'

        # print(r_email, r_phone_number, r_first_name, r_last_name)
        app.security.datastore.create_user(email=r_email, first_name=r_first_name, last_name=r_last_name)
        db.session.commit()
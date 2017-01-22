import requests
import time

r = requests.get('https://www.duolingo.com/api/1/users/show?username=MarieLB86')

user = r.json()

date_today = time.strftime('%Y-%m-%d', time.gmtime(time.time()))

def get_today_points():
    total_points = 0
    german = user['language_data']['de']
    for i in range(len(german['calendar'])):
        epoch_time = float('{0:0f}'.format(german['calendar'][i]['datetime'])[0:10])
        my_time = time.strftime('%Y-%m-%d', time.localtime(epoch_time))
        if my_time == date_today:
            my_points = user['calendar'][i]['improvement']
            total_points += my_points
    fluency = round(german['fluency_score']*100,2)
    result = [date_today, 'Duolingo', 'German', total_points, 'Points', fluency, user['site_streak']]
    return result

import requests
import json 
import os 
from icalendar import Calendar, Event

#Paramètres
user = "XXXXXX"     #à remplir
pwd = "XXXXXX"    #à remplir
n_voie = '74'   #code correspondant à la voie 3A DS SA. La liste des codes est dans la source de la page https://pamplemousse.ensae.fr/index.php?p=400
start_date = '2018-10-01'
end_date = '2019-01-18'
matieres=[381,2825,164,729,424,695,521,634,3412,4321,719]   #codes correspondants aux matières 3A DS SA. La liste des codes est dans la source de la page https://pamplemousse.ensae.fr/index.php?p=304



#Login Pamplemousse
data = {
	"sph_org_location": '/',
	"sph_username": user, 
	"sph_password": pwd, 
}
response = requests.post("https://pamplemousse.ensae.fr/site_publishing_helper/login_check/0", data=data)
cookies = {
    'cookiesession3': response.history[0].headers['Set-Cookie'].split(";")[0].split("cookiesession3=")[-1],
    'PHPSESSID': response.headers['Set-Cookie'].split(";")[0].split("=")[-1],
    'cookiesession1': response.headers['Set-Cookie'].split(";")[1].split("=")[-1],
}


#Connexion à la page d'emploi du temps
headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Origin': 'https://pamplemousse.ensae.fr',
    'Upgrade-Insecure-Requests': '1',
    'DNT': '1',
    'Content-Type': 'application/x-www-form-urlencoded',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Referer': 'https://pamplemousse.ensae.fr/index.php?p=400',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9,fr-FR;q=0.8,fr;q=0.7,ru;q=0.6,de;q=0.5,pt;q=0.4',
}
params = (
    ('p', '404'),
)
data = {
  'id_voie[]': n_voie
}
response = requests.post('https://pamplemousse.ensae.fr/index.php', headers=headers, params=params, cookies=cookies, data=data)


#Connexion au back-end chargé de l'emploi du temps
headers = {
    'Origin': 'https://pamplemousse.ensae.fr',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.9,fr-FR;q=0.8,fr;q=0.7,ru;q=0.6,de;q=0.5,pt;q=0.4',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Referer': 'https://pamplemousse.ensae.fr/index.php?p=404',
    'X-Requested-With': 'XMLHttpRequest',
    'Connection': 'keep-alive',
    'DNT': '1',
}
params = (
    ('p', '4040'),
)
data = {
  'start': start_date,
  'end': end_date
}
response = requests.post('https://pamplemousse.ensae.fr/index.php', headers=headers, params=params, cookies=cookies, data=data)


#Création du calendrier
data = json.loads(response.text)
cal = Calendar()
cal.add('prodid', '-//3A DS SA//test//')
for cours in data:
	if int(cours['id_matiere']) in matieres:
		event = Event()
		event['dtstart'] = cours['start'].replace("-", "").replace(':', '')
		event['dtend'] = cours['end'].replace("-", "").replace(':', '')
		event['summary'] = cours['title']
		cal.add_component(event)


f = open('calendrier.ics', 'wb')
f.write(cal.to_ical())
f.close()

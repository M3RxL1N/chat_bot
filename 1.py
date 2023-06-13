import discord
import requests

from bs4 import BeautifulSoup


class M3RL1N(discord.Client):
    async def on_ready(self):
        print('Logged in as {0.user}'.format(client))

    async def on_message(self, message):
        if message.author == client.user:
            return
        with open(f'{message.author}.log', 'a') as log:
            log.write(f'{message.author} - {message.content} - {message.created_at}\n')

        if message.content.startswith('!help'):
            await message.channel.send(
                'Привет! Я бот, который может предоставить тебе информацию о погоде. Вот мои команды:\n'
                '!city - узнать погоду в городе Кемерово\n'
                '!temp <название города> - узнать текущую температуру в указанном городе\n'
                '!forecast <название города> - узнать прогноз погоды на ближайшие 5 дней в указанном городе\n'
                '!about - узнать информацию о боте')

        elif message.content.startswith('!about'):
            await message.channel.send(
                'Я бот, который предоставляет информацию о погоде. Я использую API OpenWeatherMap и парсинг сайта accuweather для получения данных.')

        elif message.content.startswith('!city'):
            try:
                url = f'https://www.accuweather.com/en/ru/kemerovo/293142/weather-forecast/293142'
                header = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}
                response = requests.get(url, headers=header, timeout=10)
                soup = BeautifulSoup(response.text, 'html.parser')
                weather = soup.find('div', class_='phrase').text
                temperature = soup.find('span', class_='header-temp').text
                await message.channel.send(f'Погода в Кемерово: {weather}, температура {temperature}')
            except:
                await message.channel.send('Город не найден')

        elif message.content.startswith('!temp'):
            city = message.content.split(' ')[1]
            url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid=08efd5663387b49ddd50dd8b0a1d4a3a&units=metric'

            response = requests.get(url)
            data = response.json()

            try:
                temp = data['main']['temp']
                await message.channel.send(f'Текущая температура в городе {city}: {temp}°C')
            except:
                await message.channel.send('Город не найден')

        elif message.content.startswith('!forecast'):
            city = message.content.split(' ')[1]

            url = f'https://api.openweathermap.org/data/2.5/forecast?q={city}&appid=08efd5663387b49ddd50dd8b0a1d4a3a&units=metric'

            response = requests.get(url)
            data = response.json()

            try:
                forecast = ''
                for i in range(0, 5):
                    date = data['list'][i]['dt_txt'].split(' ')[0]
                    time = data['list'][i]['dt_txt'].split(' ')[1][:5]
                    temp = data['list'][i]['main']['temp']
                    weather = data['list'][i]['weather'][0]['description']
                    forecast += f'{date} {time}: {temp}°C, {weather}\n'

                await message.channel.send(f'Прогноз погоды в городе {city} на ближайшие 5 дней:\n{forecast}')
            except:
                await message.channel.send('Город не найден')


intents = discord.Intents.default()
intents.members = True
intents.message_content = True
client = M3RL1N(intents=intents)

client.run('MTEwOTg3NTM3ODU4MDg4NTU1NA.Gwc6Jj.8cZ430ijlsqQeF-dX4v-WtmRjOKLbCNEI-GNXM')

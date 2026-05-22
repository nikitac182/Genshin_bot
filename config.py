from dotenv import load_dotenv
import os

load_dotenv()

TOKEN = os.getenv('TOKEN')
ADMIN_ID = [1143200581, 1094046982]
ADMIN_USERNAME = ['@Nekitnnn', '@Gods_GG']

commands = {
    '/start': ('Запустить бота',),
    '/help': ('Показать это сообщение',),
    '/add_primogems': (
        'Добавить примогемы',
    ),
    '/wishes': ('Показать историю круток',),
    '/shop': ('Показать магазин',),
}
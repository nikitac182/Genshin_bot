import random
from typing import Dict, List

class GachaRandomizer:
    def __init__(self, banner_type: str = "characters"):
        self.banner_type = banner_type
        self.load_items()
    
    def load_items(self):

        self.weapons_3star = [
            "Посыльный", "Рогатка", "Изогнутый лук", "Клятва стрелка", 
            "Лук ворона", "Изумрудный шар", "Потусторонняя история", 
            "Эпос о драконоборцах", "Руководство по магии", "Чёрная кисть",
            "Дубина переговоров", "Меч из белого железа", "Меч драконьей крови", 
            "Металлическая тень", "Меч путешественника", "Предвестник зари"
        ]

        self.characters_4star = [
            "Прюн", "Иллуги", "Ягода", "Айно", "Далия", "Ифа", 
            "Иансан", "Лань Янь", "Оророн", "Качина", "Сетос", 
            "Ка Мин", "Шеврёз", "Шарлотта", "Фремине", "Линетт", 
            "Кавех", "Мика", "Яо Яо", "Фарузан", "Лайла", "Кандакия", 
            "Дори", "Коллеи", "Синобу", "Юнь Цзинь", "Кирара", 
            "Хэйдзо", "Сара", "Горо", "Саю", "Тома", "Янь Фэй", 
            "Розария", "Синь Янь", "Сахароза", "Диона", "Чун Юнь", 
            "Ноэлль", "Беннет", "Фишль", "Нин Гуан", "Син Цю", 
            "Бэй Доу", "Сян Лин", "Эмбер", "Рэйзор", "Кэйа", "Барбара", "Лиза"
        ]

        self.standard_5star_characters = [
            "Дэхья", "Ци Ци", "Кэ Цин", "Тигнари", 
            "Дилюк", "Джинн", "Мидзуки"
        ]

        self.banner_5star_characters = [
            "Николь", "Линнея", "Лоэн", "Варка", "Цзы Бай", "Коломбина", 
            "Дурин", "Нефер", "Флинс", "Лаума", "Инеффа", "Скирк", "Эскофье", 
            "Вареса", "Ситлали", "Мавуика", "Часка", "Шилонен", "Муалани", 
            "Кинич", "Эмилия", "Клоринда", "Арлекино", "Сиджвин", "Тиори", 
            "Сянь Юнь", "Навия", "Фурина", "Нёвиллет", "Ризли", "Лини", 
            "Бай Чжу", "Аль-Хайтам", "Странник", "Нахида", "Сайно", "Нилу", 
            "Аято", "Шэнь Хэ", "Е Лань", "Яэ Мико", "Итто", "Кокоми", "Райдэн", 
            "Эола", "Ёимия", "Кадзуха", "Ху Тао", "Мона", "Альбедо", "Гань Юй", 
            "Тарталья", "Чжун Ли", "Аяка", "Сяо", "Венти"
        ]

        self.all_5star_characters = self.standard_5star_characters + self.banner_5star_characters

        self.weapons_4star = [
            "Разбивающий цепи", "Дальномер", "Луна Моун", "Охотник во тьме", 
            "Ржавый лук", "Церемониальный лук", "Бесструнный", "Боевой лук Фавония", 
            "Рассветный иней", "Вихрь на волнах", "Скитающаяся звезда", 
            "Вино и песни", "Око сознания", "Церемониальные мемуары", 
            "Песнь странника", "Кодекс Фавония", "Посох жертвующей", 
            "Крепящий горы шип", "Бур рудоискателя", "Режущий волны плавник", 
            "Копьё Фавония", "Каменное копьё", "Гроза драконов", "Плодотворный крюк", 
            "Акуомару", "Аквамарин Махайры", "Каменный меч", 
            "Церемониальный двуручный меч", "Меч-колокол", "Двуручный меч Фавония", 
            "Рассвет прядильщицы луны", "Лунное сияние ксифоса", "Вспышка во тьме", 
            "Драконий рык", "Церемониальный меч", "Меч-флейта", "Меч Фавония"
        ]

        self.banner_weapons_5star = [
            "Золотая клятва льда", "Хроники рассвета", "Алое перо звёздного грифа", 
            "Сердечные струны дождя", "Первый великий фокус", "Охотничья тропа", 
            "Громовой пульс", "Аква симулякрум", "Полярная звезда", "Элегия погибели", 
            "Гептада ангела", "Вызов ноктюрна",
            "Шкатулка истин", "Зеркало прядильщицы ночи", "Переливающиеся чаяния", 
            "Сон солнечным утром", "Бдение взывающего к звёздам", "Лови волну", 
            "Звонкий клич журавля", "Обряд вечного течения", "Казначейский надзор", 
            "Воспоминания Тулайтуллы", "Сновидения тысячи ночей", "Истина кагура", 
            "Вечное лунное сияние", "Великолепие лазурного свода", "Память о пыли", 
            "Бедствие и раскаяние", "Окровавленные руины", "Расколотый ореол", 
            "Симфонист ароматов", "Элегия Люмидус", "Очертания алой луны", 
            "Посох алых песков", "Сияющая жатва", "Усмиритель бед", 
            "Покоритель вихря", "Посох Хомы", "Некованый",
            "Подвиг могучего волка", "Тысяча ослепительных солнц", "Клык Горного короля", 
            "Вердикт", "Маяк тростникового моря", "Краснорогий камнеруб", 
            "Песнь разбитых сосен", "Светоносный осколок луны", "Атаме артис", 
            "Лазурное сияние", "Песнь патруля пиков", "Отпущение грехов", "Ураку мисугири", 
            "Блеск тихих вод", "Свет лиственного разреза", "Ключ Хадж-нисут", 
            "Харан гэппаку фуцу", "Рассекающий туман", "Драгоценный омут", 
            "Кромсатель пиков", "Клятва свободы", 
        ]

        self.standart_weapons_5star = [
            "Небесный меч", "Нефритовый коршун", "Волчья погибель", "Небесное величие",
            "Лук Амоса", "Небесное крыло", "Молитва святым ветрам", "Небесный атлас",
            "Небесная ось", "Меч Сокола"
        ]

        self.all_5star_weapons = self.banner_weapons_5star + self.standart_weapons_5star
    
    def get_3star(self) -> Dict:
        return {
            "name": random.choice(self.weapons_3star),
            "type": "weapon",
            "rarity": 3
        }
    
    def get_4star(self, guarantee: bool = False) -> Dict:
        if self.banner_type == "weapons":
            if guarantee:
                return {
                        "name": random.choice(self.weapons_4star),
                        "type": "weapon",
                        "rarity": 4
                    }
            else:
                if random.random() < 0.75:
                    return {
                        "name": random.choice(self.weapons_4star),
                        "type": "weapon",
                        "rarity": 4
                    }
                else:
                    return {
                        "name": random.choice(self.characters_4star),
                        "type": "character",
                        "rarity": 4
                    }
        else:
            if guarantee:
                return {
                    "name": random.choice(self.characters_4star),
                    "type": "character",
                    "rarity": 4
                }
            else:
                if random.random() < 0.5:
                    return {
                        "name": random.choice(self.characters_4star),
                        "type": "character",
                        "rarity": 4
                    }
                else:
                    return {
                        "name": random.choice(self.weapons_4star),
                        "type": "weapon",
                        "rarity": 4
                    }
    
    def get_5star(self, guarantee: bool = False) -> Dict:
        if self.banner_type == "weapons":
            if guarantee:
                return {
                        "name": random.choice(self.banner_weapons_5star),
                        "type": "weapon",
                        "rarity": 5
                    }
            else:
                if random.random() < 0.75:
                    return {
                        "name": random.choice(self.banner_weapons_5star),
                        "type": "weapon",
                        "rarity": 5
                    }
                else:
                    return {
                        "name": random.choice(self.standart_weapons_5star),
                        "type": "weapon",
                        "rarity": 5
                    }
        elif self.banner_type == "characters":
            if guarantee:
                return {
                    "name": random.choice(self.banner_5star_characters),
                    "type": "character",
                    "rarity": 5
                }
            else:
                if random.random() < 0.5:
                    return {
                        "name": random.choice(self.banner_5star_characters),
                        "type": "character",
                        "rarity": 5
                    }
                else:
                    return {
                        "name": random.choice(self.standard_5star_characters),
                        "type": "character",
                        "rarity": 5
                    }
        else:
            if random.random() < 0.5:
                return {
                    "name": random.choice(self.all_5star_characters),
                    "type": "character",
                    "rarity": 5
                }
            else:
                return {
                    "name": random.choice(self.all_5star_weapons),
                    "type": "weapon",
                    "rarity": 5
                }
    
    def set_banner(self, banner_type: str):
        if banner_type in ["characters", "weapons", "standard"]:
            self.banner_type = banner_type
            return True
        return False

    def get_banner_info(self) -> str:
        
        if self.banner_type == "characters":
            return "👥 Только 5★ персонажи"
        elif self.banner_type == "weapons":
            return "⚔️ Только 5★ оружие"
        else:
            return "⭐ Все 5★ персонажи и оружия"


def get_random_weapon_by_rarity(rarity: int) -> str:
    gacha = GachaRandomizer()
    if rarity == 3:
        pool = gacha.weapons_3star
    elif rarity == 4:
        pool = gacha.weapons_4star
    elif rarity == 5:
        pool = gacha.all_5star_weapons
    else:
        return "Неизвестное оружие"
    
    return random.choice(pool)


def get_random_character_by_rarity(rarity: int) -> str:
    gacha = GachaRandomizer()
    if rarity == 4:
        pool = gacha.characters_4star
    elif rarity == 5:
        pool = gacha.all_5star_characters
    else:
        return "Неизвестный персонаж"
    
    return random.choice(pool)


def get_all_5star_characters() -> List[str]:
    return GachaRandomizer().all_5star_characters

def get_all_5star_weapons() -> List[str]:
    return GachaRandomizer().all_5star_weapons
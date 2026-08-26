from django.core.management.base import BaseCommand
from shop.models import Category, Product


class Command(BaseCommand):
    help = "Наповнює базу даних новими тематичними товарами для Rare Find"

    def handle(self, *args, **kwargs):
        self.stdout.write("Очищення старої бази даних...")
        Product.objects.all().delete()
        Category.objects.all().delete()

        self.stdout.write("Починаємо створення тематичних даних для Rare Find...")

        categories_structure = {
            "Стежки Вітру": ["Крилаті Сандалії", "Обладунки Швидкості", "Амулети Бігуна"],
            "Кулак Титана": ["Бойові Наручі", "Щити Захисту"],
            "Рівновага Духу": ["Сувої Левітації", "Магічні Снаряди"],
            "Водна Стихія": ["Окуляри Водяного", "Аква-Обладунки"],
            "Двоколісні Пегаси": ["Залізні Пегаси", "Шоломи Безпеки"],
            "Братство Гри": ["Сфера Гри", "Високий Політ"],
            "Загадкові Знахідки": [],
        }

        category_map = {}

        for parent_name, children in categories_structure.items():
            parent_cat, _ = Category.objects.get_or_create(
                name=parent_name, parent=None
            )
            category_map[parent_name] = parent_cat

            for child_name in children:
                child_cat, _ = Category.objects.get_or_create(
                    name=child_name, parent=parent_cat
                )
                category_map[child_name] = child_cat

        products_data = [
            # ── Стежки Вітру ──
            {"name": "Кросівки Kiprun KS900", "slug": "krosivky-kiprun-ks900", "cat": "Крилаті Сандалії", "price": 3499.00,
             "description": "Посилені сандалії для швидкого бігу з повітряною амортизацією."},
            {"name": "Кросівки Run Cushion", "slug": "krosivky-run-cushion", "cat": "Крилаті Сандалії", "price": 1299.00,
             "description": "Зручне взуття для перших кроків на шляху до нових обріїв."},
            {"name": "Футболка Run Dry+", "slug": "futbolka-run-dry-plus", "cat": "Обладунки Швидкості", "price": 449.00,
             "description": "Дихаюча туніка, що відводить вологу під час шаленого бігу."},
            {"name": "Шорти для бігу Run 100", "slug": "shorty-run-100", "cat": "Обладунки Швидкості", "price": 399.00,
             "description": "Легкі шорти для вільного руху за вітром."},
            {"name": "Шкарпетки для бігу Run900 2 пари", "slug": "shkarpetky-run900", "cat": "Амулети Бігуна", "price": 249.00,
             "description": "Захисні обгортки для стоп із підтримкою склепіння."},
            {"name": "Пояс для бігу Kiprun", "slug": "poias-dlia-bihu-kiprun", "cat": "Амулети Бігуна", "price": 599.00,
             "description": "Зручний ремінь для перенесення артефактів зв'язку та ключів."},

            # ── Кулак Титана ──
            {"name": "Боксерські рукавиці Outshock 500", "slug": "outshock-500", "cat": "Бойові Наручі", "price": 1299.00,
             "description": "Шкіряні наручі для надійного захисту кулаків під час бою."},
            {"name": "Рукавиці для снарядів Outshock 100", "slug": "outshock-100", "cat": "Бойові Наручі", "price": 699.00,
             "description": "Полегшені бойові рукавиці для відпрацювання ударів."},
            {"name": "Капа боксерська ERGO 500", "slug": "kapa-ergo-500", "cat": "Щити Захисту", "price": 249.00,
             "description": "Захисний щиток для зубів та щелепи."},
            {"name": "Бинти боксерські 4м", "slug": "bynty-bokserski-4m", "cat": "Щити Захисту", "price": 199.00,
             "description": "Еластична стрічка для фіксації та зміцнення суглобів."},
            {"name": "Шолом боксерський 500", "slug": "shlem-bokserskyi-500", "cat": "Щити Захисту", "price": 1599.00,
             "description": "Повний шолом для захисту голови від ворожих ударів."},

            # ── Рівновага Духу ──
            {"name": "Килимок для йоги Essential 8мм", "slug": "kylymok-yoga-8mm", "cat": "Сувої Левітації", "price": 799.00,
             "description": "Стабільний сувій для медитації та єднання з космосом."},
            {"name": "Килимок для фітнесу Comfort 15мм", "slug": "kylymok-fitness-15mm", "cat": "Сувої Левітації", "price": 1199.00,
             "description": "Потовщений м'який сувій для складних практик."},
            {"name": "Гантелі для фітнесу 2х2 кг", "slug": "hanteli-2x2kg", "cat": "Магічні Снаряди", "price": 649.00,
             "description": "Важкі сфери для зміцнення м'язів рук."},
            {"name": "Фітнес-резинки набор 3 шт", "slug": "retynky-fitness-3pcs", "cat": "Магічні Снаряди", "price": 349.00,
             "description": "Еластичні стрічки опору для тренування сили."},
            {"name": "М'яч для фітнесу Swiss Ball 65см", "slug": "swiss-ball-65cm", "cat": "Магічні Снаряди", "price": 549.00,
             "description": "Велика пружна сфера для тренування балансу."},

            # ── Водна Стихія ──
            {"name": "Окуляри для плавання Nabaiji Xbase", "slug": "nabaiji-xbase", "cat": "Окуляри Водяного", "price": 229.00,
             "description": "Окуляри, що дозволяють бачити під водою без перешкод."},
            {"name": "Шапочка для плавання силіконова", "slug": "shapochka-silicone", "cat": "Окуляри Водяного", "price": 179.00,
             "description": "Захисний обтічний шолом для плавання."},
            {"name": "Плавки-шорти 100 Basic", "slug": "plavky-shorty-100", "cat": "Аква-Обладунки", "price": 399.00,
             "description": "Швидковисихаючий одяг для підкорення хвиль."},
            {"name": "Купальник суцільний Heva", "slug": "kupalnyk-heva", "cat": "Аква-Обладунки", "price": 699.00,
             "description": "Суцільний аква-костюм для тривалого перебування у воді."},

            # ── Двоколісні Пегаси ──
            {"name": "Гірський велосипед Rockrider ST100", "slug": "rockrider-st100", "cat": "Залізні Пегаси", "price": 11999.00,
             "description": "Сталевий пегас для швидкого долання гірських стежок."},
            {"name": "Шолом шосейний Roadr 500", "slug": "sholom-roadr-500", "cat": "Шоломи Безпеки", "price": 1499.00,
             "description": "Обтічний шолом для захисту голови вершника."},
            {"name": "Перчатки велосипедні Btwin 100", "slug": "perchatky-btwin-100", "cat": "Шоломи Безпеки", "price": 299.00,
             "description": "Рукавички для надійного зчеплення з кермом залізного коня."},

            # ── Братство Гри ──
            {"name": "М'яч футбольний Kipsta F100", "slug": "myach-kipsta-f100", "cat": "Сфера Гри", "price": 499.00,
             "description": "Сфера для командних ігор на трав'яних полях."},
            {"name": "Бутси для штучного покриття Agility 100", "slug": "butsy-agility-100", "cat": "Сфера Гри", "price": 999.00,
             "description": "Бутси з шипами для кращої стійкості під час матчів."},
            {"name": "М'яч баскетбольний Tarmak BT100", "slug": "tarmak-bt100", "cat": "Високий Політ", "price": 599.00,
             "description": "Пружна сфера для точних кидків у кошик."},
            {"name": "Щитки футбольні F500", "slug": "shchytky-f500", "cat": "Сфера Гри", "price": 349.00,
             "description": "Надійні пластини для захисту гомілок."},

            # ── Загадкові Знахідки ──
            {
                "name": "Антигравітаційний Годинник",
                "slug": "antyhravitaciinyi-hodinnyk",
                "cat": "Загадкові Знахідки",
                "price": 7777.00,
                "description": "Годинник, стрілки якого рухаються у зворотному напрямку. Кажуть, його власник починає відчувати час інакше — хвилини розтягуються в моменти щастя і стискаються в нудні дні.",
                "is_mysterious": True,
                "rarity": "legend",
            },
            {
                "name": "Компас Забутих Шляхів",
                "slug": "kompas-zabutykh-shliakhiv",
                "cat": "Загадкові Знахідки",
                "price": 4999.00,
                "description": "Давній артефакт, що вказує не на північ, а на найближчу таємницю. Стрілка тремтить сильніше, коли ви наближаєтеся до чогось незвичайного.",
                "is_mysterious": True,
                "rarity": "epic",
            },
            {
                "name": "Еліксир Вічної Витривалості",
                "slug": "eliksyr-vichnoi-vytryvalosti",
                "cat": "Загадкові Знахідки",
                "price": 2499.00,
                "description": "Кришталева пляшечка з мерехтливою рідиною, яка змінює колір залежно від настрою того, хто її тримає.",
                "is_mysterious": True,
                "rarity": "rare",
            },
            {
                "name": "Окуляри Істинного Зору",
                "slug": "okuliaryistynoho-zoru",
                "cat": "Загадкові Знахідки",
                "price": 5555.00,
                "description": "Ці окуляри з лінзами, відлитими з вулканічного скла, дозволяють бачити приховані деталі навколишнього світу.",
                "is_mysterious": True,
                "rarity": "legend",
            },
            {
                "name": "Сувій Прадавньої Мудрості",
                "slug": "suvii-pradavnoi-mudrosti",
                "cat": "Загадкові Знахідки",
                "price": 3333.00,
                "description": "Пергаментний сувій, вкритий письменами, які ніхто не може розшифрувати повністю. Кожен читач бачить у них щось своє.",
                "is_mysterious": True,
                "rarity": "epic",
            },
            {
                "name": "Сфера Нічного Неба",
                "slug": "sfera-nichnoho-neba",
                "cat": "Загадкові Знахідки",
                "price": 6200.00,
                "description": "Скляна куля, всередині якої мерехтять крихітні вогники, що повторюють розташування зірок поточної ночі.",
                "is_mysterious": True,
                "rarity": "legend",
            },
            {
                "name": "Рукавички Вітру",
                "slug": "rukavychky-vitru",
                "cat": "Загадкові Знахідки",
                "price": 1899.00,
                "description": "Тонкі шовкові рукавички, в яких руки ніколи не мерзнуть і не потіють. Тканина переливається на світлі.",
                "is_mysterious": True,
                "rarity": "rare",
            },
            {
                "name": "Дзвіночок Тиші",
                "slug": "dzvinochok-tyshi",
                "cat": "Загадкові Знахідки",
                "price": 999.00,
                "description": "Маленький бронзовий дзвіночок, який не видає жодного звуку при дзвонінні. Але всі поруч відчувають глибокий внутрішній спокій.",
                "is_mysterious": True,
                "rarity": "common",
            },
        ]

        created_count = 0
        for p in products_data:
            cat_obj = category_map[p["cat"]]
            product, created = Product.objects.get_or_create(
                slug=p["slug"],
                defaults={
                    "name": p["name"],
                    "category": cat_obj,
                    "price": p["price"],
                    "description": p.get("description", ""),
                    "is_mysterious": p.get("is_mysterious", False),
                    "rarity": p.get("rarity", "common"),
                },
            )
            if created:
                created_count += 1

        self.stdout.write(
            self.style.SUCCESS(f"Успішно створено {created_count} нових товарів із новою схемою назв!")
        )
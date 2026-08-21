from django.core.management.base import BaseCommand
from shop.models import Category, Product


class Command(BaseCommand):
    help = "Наповнює базу даних тестовими товарами для Rare Find"

    def handle(self, *args, **kwargs):
        self.stdout.write("Починаємо створення тестових даних для Rare Find...")

        categories_structure = {
            "Біг": ["Кросівки", "Одяг для бігу", "Аксесуари для бігу"],
            "Бокс та єдиноборства": ["Рукавиці", "Захист"],
            "Фітнес і йога": ["Килимки", "Інвентар"],
            "Плавання": ["Окуляри та шапочки", "Плавки та купальники"],
            "Велоспорт": ["Велосипеди", "Шоломи та захист"],
            "Командні види спорту": ["Футбол", "Баскетбол"],
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
            # ── Звичайні товари ──
            {"name": "Кросівки Kiprun KS900", "slug": "krosivky-kiprun-ks900", "cat": "Кросівки", "price": 3499.00,
             "description": "Легкі бігові кросівки з амортизацією для тренувань."},
            {"name": "Кросівки Run Cushion", "slug": "krosivky-run-cushion", "cat": "Кросівки", "price": 1299.00,
             "description": "Зручні повсякденні кросівки для початківців."},
            {"name": "Футболка Run Dry+", "slug": "futbolka-run-dry-plus", "cat": "Одяг для бігу", "price": 449.00,
             "description": "Дихаюча футболка з технологією швидкого висихання."},
            {"name": "Шорти для бігу Run 100", "slug": "shorty-run-100", "cat": "Одяг для бігу", "price": 399.00,
             "description": "Легкі шорти для комфортного бігу."},
            {"name": "Шкарпетки для бігу Run900 2 пари", "slug": "shkarpetky-run900", "cat": "Аксесуари для бігу", "price": 249.00,
             "description": "Технічні шкарпетки з підтримкою склепіння."},
            {"name": "Пояс для бігу Kiprun", "slug": "poias-dlia-bihu-kiprun", "cat": "Аксесуари для бігу", "price": 599.00,
             "description": "Ергономічний пояс для зберігання телефону та ключів."},

            {"name": "Боксерські рукавиці Outshock 500", "slug": "outshock-500", "cat": "Рукавиці", "price": 1299.00,
             "description": "Рукавиці зі зносостійкої штучної шкіри для тренувань."},
            {"name": "Рукавиці для снарядів Outshock 100", "slug": "outshock-100", "cat": "Рукавиці", "price": 699.00,
             "description": "Легкі рукавиці для роботи зі снарядами."},
            {"name": "Капа боксерська ERGO 500", "slug": "kapa-ergo-500", "cat": "Захист", "price": 249.00,
             "description": "Ергономічна капа для захисту зубів."},
            {"name": "Бинти боксерські 4м", "slug": "bynty-bokserski-4m", "cat": "Захист", "price": 199.00,
             "description": "Еластичні бинти для фіксації зап'ястка."},
            {"name": "Шлем боксерський 500", "slug": "shlem-bokserskyi-500", "cat": "Захист", "price": 1599.00,
             "description": "Шлем з посиленим захистом скронь та підборіддя."},

            {"name": "Килимок для йоги Essential 8мм", "slug": "kylymok-yoga-8mm", "cat": "Килимки", "price": 799.00,
             "description": "Нековзний килимок для комфортної практики."},
            {"name": "Килимок для фітнесу Comfort 15мм", "slug": "kylymok-fitness-15mm", "cat": "Килимки", "price": 1199.00,
             "description": "Товстий килимок з підвищеним комфортом."},
            {"name": "Гантелі для фітнесу 2×2 кг", "slug": "hanteli-2x2kg", "cat": "Інвентар", "price": 649.00,
             "description": "Набір вінілових гантелей для домашніх тренувань."},
            {"name": "Фітнес-резинки набір 3 шт", "slug": "retynky-fitness-3pcs", "cat": "Інвентар", "price": 349.00,
             "description": "Три рівні опору для різних вправ."},
            {"name": "М'яч для фітнесу Swiss Ball 65см", "slug": "swiss-ball-65cm", "cat": "Інвентар", "price": 549.00,
             "description": "Протирозривний м'яч для фітнесу та реабілітації."},

            {"name": "Окуляри для плавання Nabaiji Xbase", "slug": "nabaiji-xbase", "cat": "Окуляри та шапочки", "price": 229.00,
             "description": "Зручні окуляри з антизапотівальним покриттям."},
            {"name": "Шапочка для плавання силіконова", "slug": "shapochka-silicone", "cat": "Окуляри та шапочки", "price": 179.00,
             "description": "Еластична силіконова шапочка."},
            {"name": "Плавки-шорти 100 Basic", "slug": "plavky-shorty-100", "cat": "Плавки та купальники", "price": 399.00,
             "description": "Шорти для плавання зі швидковисихаючої тканини."},
            {"name": "Купальник суцільний Heva", "slug": "kupalnyk-heva", "cat": "Плавки та купальники", "price": 699.00,
             "description": "Стійкий до хлору суцільний купальник."},

            {"name": "Гірський велосипед Rockrider ST100", "slug": "rockrider-st100", "cat": "Велосипеди", "price": 11999.00,
             "description": "Надійний гірський велосипед для бездоріжжя."},
            {"name": "Шолом шосейний Roadr 500", "slug": "sholom-roadr-500", "cat": "Шоломи та захист", "price": 1499.00,
             "description": "Аеродинамічний шолом з вентиляцією."},
            {"name": "Перчатки велосипедні Btwin 100", "slug": "perchatky-btwin-100", "cat": "Шоломи та захист", "price": 299.00,
             "description": "Легкі рукавички з гелевими подушечками."},

            {"name": "М'яч футбольний Kipsta F100", "slug": "myach-kipsta-f100", "cat": "Футбол", "price": 499.00,
             "description": "Тренувальний м'яч для будь-яких покриттів."},
            {"name": "Бутси для штучного покриття Agility 100", "slug": "butsy-agility-100", "cat": "Футбол", "price": 999.00,
             "description": "Бутси з мікрошипами для штучної трави."},
            {"name": "М'яч баскетбольний Tarmak BT100", "slug": "tarmak-bt100", "cat": "Баскетбол", "price": 599.00,
             "description": "Гумовий баскетбольний м'яч для відкритих майданчиків."},
            {"name": "Щитки футболні F500", "slug": "shchytky-f500", "cat": "Футбол", "price": 349.00,
             "description": "Легкі щитки з EVA-підкладкою."},

            # ══════════════════════════════════════════════
            # ЗАГАДКОВІ ТОВАРИ (Mysterious Items)
            # ══════════════════════════════════════════════
            {
                "name": "Антигравітаційний Годинник",
                "slug": "antyhravitaciinyi-hodinnyk",
                "cat": "Загадкові Знахідки",
                "price": 7777.00,
                "description": "Годинник, стрілки якого рухаються у зворотному напрямку. "
                               "Кажуть, його власник починає відчувати час інакше — хвилини "
                               "розтягуються в моменти щастя і стискаються в нудні дні. "
                               "Знайдений на горищі старовинної обсерваторії у Карпатах.",
                "is_mysterious": True,
                "rarity": "legend",
            },
            {
                "name": "Компас Забутих Шляхів",
                "slug": "kompas-zabutykh-shliakhiv",
                "cat": "Загадкові Знахідки",
                "price": 4999.00,
                "description": "Давній артефакт, що вказує не на північ, а на найближчу таємницю. "
                               "Стрілка тремтить сильніше, коли ви наближаєтеся до чогось незвичайного. "
                               "Попередній власник стверджував, що знайшов завдяки ньому три скарби.",
                "is_mysterious": True,
                "rarity": "epic",
            },
            {
                "name": "Еліксир Вічної Витривалості",
                "slug": "eliksyr-vichnoi-vytryvalosti",
                "cat": "Загадкові Знахідки",
                "price": 2499.00,
                "description": "Кришталева пляшечка з мерехтливою рідиною, яка змінює колір "
                               "залежно від настрою того, хто її тримає. Стародавній рецепт "
                               "передавався з покоління в покоління горськими алхіміками. "
                               "Вміст: невідомо. Ефект: непередбачуваний.",
                "is_mysterious": True,
                "rarity": "rare",
            },
            {
                "name": "Окуляри Істинного Зору",
                "slug": "okuliaryistynoho-zoru",
                "cat": "Загадкові Знахідки",
                "price": 5555.00,
                "description": "Ці окуляри з лінзами, відлитими з вулканічного скла, дозволяють "
                               "бачити приховані деталі навколишнього світу. Кажуть, крізь них "
                               "можна прочитати стерті написи та побачити невидимі стежки. "
                               "Побічний ефект: реальність стає цікавішою.",
                "is_mysterious": True,
                "rarity": "legend",
            },
            {
                "name": "Сувій Прадавньої Мудрості",
                "slug": "suvii-pradavnoi-mudrosti",
                "cat": "Загадкові Знахідки",
                "price": 3333.00,
                "description": "Пергаментний сувій, вкритий письменами, які ніхто не може "
                               "розшифрувати повністю. Кожен читач бачить у них щось своє — "
                               "хтось формулу успіху, хтось вірш, а хтось рецепт найкращого борщу. "
                               "Датується орієнтовно XII століттям.",
                "is_mysterious": True,
                "rarity": "epic",
            },
            {
                "name": "Сфера Нічного Неба",
                "slug": "sfera-nichnoho-neba",
                "cat": "Загадкові Знахідки",
                "price": 6200.00,
                "description": "Скляна куля, всередині якої мерехтять крихітні вогники, "
                               "що повторюють розташування зірок поточної ночі. Ніхто не знає, "
                               "як вона працює — батарейок немає, механізму теж. "
                               "Ідеальний подарунок для мрійника.",
                "is_mysterious": True,
                "rarity": "legend",
            },
            {
                "name": "Рукавички Вітру",
                "slug": "rukavychky-vitru",
                "cat": "Загадкові Знахідки",
                "price": 1899.00,
                "description": "Тонкі шовкові рукавички, в яких руки ніколи не мерзнуть "
                               "і не потіють. Тканина переливається на світлі невидимими "
                               "візерунками. Попередній власник — мандрівний фокусник із Праги.",
                "is_mysterious": True,
                "rarity": "rare",
            },
            {
                "name": "Дзвіночок Тиші",
                "slug": "dzvinochok-tyshi",
                "cat": "Загадкові Знахідки",
                "price": 999.00,
                "description": "Маленький бронзовий дзвіночок, який не видає жодного звуку "
                               "при дзвонінні. Але всі, хто знаходиться поруч, раптово "
                               "відчувають глибокий внутрішній спокій. Знайдений у руїнах "
                               "тибетського монастиря.",
                "is_mysterious": True,
                "rarity": "common",
            },
        ]

        created_count = 0
        updated_count = 0
        for p in products_data:
            cat_obj = category_map[p["cat"]]
            defaults = {
                "name": p["name"],
                "category": cat_obj,
                "price": p["price"],
                "description": p.get("description", ""),
                "is_mysterious": p.get("is_mysterious", False),
                "rarity": p.get("rarity", "common"),
            }
            product, created = Product.objects.get_or_create(
                slug=p["slug"],
                defaults=defaults,
            )
            if created:
                created_count += 1
            else:
                # Update existing products with new fields
                changed = False
                for field, value in defaults.items():
                    if getattr(product, field) != value:
                        setattr(product, field, value)
                        changed = True
                if changed:
                    product.save()
                    updated_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Готово! Створено {created_count} нових товарів, "
                f"оновлено {updated_count} існуючих."
            )
        )
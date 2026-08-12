from django.core.management.base import BaseCommand
from shop.models import Category, Product


class Command(BaseCommand):
    help = "Наповнює базу даних 25+ тестовими товарами Decathlon"

    def handle(self, *args, **kwargs):
        self.stdout.write("Починаємо створення тестових даних...")

        categories_structure = {
            "Біг": ["Кросівки", "Одяг для бігу", "Аксесуари для бігу"],
            "Бокс та єдиноборства": ["Рукавиці", "Захист"],
            "Фітнес і йога": ["Килимки", "Інвентар"],
            "Плавання": ["Окуляри та шапочки", "Плавки та купальники"],
            "Велоспорт": ["Велосипеди", "Шоломи та захист"],
            "Командні види спорту": ["Футбол", "Баскетбол"],
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

            {"name": "Кросівки Kiprun KS900", "slug": "krosivky-kiprun-ks900", "cat": "Кросівки", "price": 3499.00},
            {"name": "Кросівки Run Cushion", "slug": "krosivky-run-cushion", "cat": "Кросівки", "price": 1299.00},
            {"name": "Футболка Run Dry+", "slug": "futbolka-run-dry-plus", "cat": "Одяг для бігу", "price": 449.00},
            {"name": "Шорти для бігу Run 100", "slug": "shorty-run-100", "cat": "Одяг для бігу", "price": 399.00},
            {"name": "Шкарпетки для бігу Run900 2 пари", "slug": "shkarpetky-run900", "cat": "Аксесуари для бігу", "price": 249.00},
            {"name": "Пояс для бігу Kiprun", "slug": "poias-dlia-bihu-kiprun", "cat": "Аксесуари для бігу", "price": 599.00},

            {"name": "Боксерські рукавиці Outshock 500", "slug": "outshock-500", "cat": "Рукавиці", "price": 1299.00},
            {"name": "Рукавиці для снарядів Outshock 100", "slug": "outshock-100", "cat": "Рукавиці", "price": 699.00},
            {"name": "Капа боксерська ERGO 500", "slug": "kapa-ergo-500", "cat": "Захист", "price": 249.00},
            {"name": "Бинти боксерські 4м", "slug": "bynty-bokserski-4m", "cat": "Захист", "price": 199.00},
            {"name": "Шлем боксерський 500", "slug": "shlem-bokserskyi-500", "cat": "Захист", "price": 1599.00},

            {"name": "Килимок для йоги Essential 8мм", "slug": "kylymok-yoga-8mm", "cat": "Килимки", "price": 799.00},
            {"name": "Килимок для фітнесу Comfort 15мм", "slug": "kylymok-fitness-15mm", "cat": "Килимки", "price": 1199.00},
            {"name": "Гантелі для фітнесу 2х2 кг", "slug": "hanteli-2x2kg", "cat": "Інвентар", "price": 649.00},
            {"name": "Фітнес-резинки набор 3 шт", "slug": "retynky-fitness-3pcs", "cat": "Інвентар", "price": 349.00},
            {"name": "М'яч для фітнесу Swiss Ball 65см", "slug": "swiss-ball-65cm", "cat": "Інвентар", "price": 549.00},

            {"name": "Окуляри для плавання Nabaiji Xbase", "slug": "nabaiji-xbase", "cat": "Окуляри та шапочки", "price": 229.00},
            {"name": "Шапочка для плавання силіконова", "slug": "shapochka-silicone", "cat": "Окуляри та шапочки", "price": 179.00},
            {"name": "Плавки-шорти 100 Basic", "slug": "plavky-shorty-100", "cat": "Плавки та купальники", "price": 399.00},
            {"name": "Купальник суцільний Heva", "slug": "kupalnyk-heva", "cat": "Плавки та купальники", "price": 699.00},

            {"name": "Гірський велосипед Rockrider ST100", "slug": "rockrider-st100", "cat": "Велосипеди", "price": 11999.00},
            {"name": "Шолом шосейний Roadr 500", "slug": "sholom-roadr-500", "cat": "Шоломи та захист", "price": 1499.00},
            {"name": "Перчатки велосипедні Btwin 100", "slug": "perchatky-btwin-100", "cat": "Шоломи та захист", "price": 299.00},

            {"name": "М'яч футбольний Kipsta F100", "slug": "myach-kipsta-f100", "cat": "Футбол", "price": 499.00},
            {"name": "Бутси для штучного покриття Agility 100", "slug": "butsy-agility-100", "cat": "Футбол", "price": 999.00},
            {"name": "М'яч баскетбольний Tarmak BT100", "slug": "tarmak-bt100", "cat": "Баскетбол", "price": 599.00},
            {"name": "Щитки футболні F500", "slug": "shchytky-f500", "cat": "Футбол", "price": 349.00},
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
                },
            )
            if created:
                created_count += 1

        self.stdout.write(
            self.style.SUCCESS(f"Успішно створено {created_count} нових товарів!")
        )
        
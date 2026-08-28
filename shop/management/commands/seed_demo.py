from shop.management.commands.populate_db import Command as PopulateDbCommand


class Command(PopulateDbCommand):
    help = "Аліас для populate_db: наповнює базу демонстраційними даними"

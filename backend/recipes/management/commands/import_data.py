import csv
import json

from django.conf import settings
from django.core.management.base import BaseCommand

from recipes.models import Ingredient, Tag


class Command(BaseCommand):
    def handle(self, *args, **options):
        filenames = {
            Ingredient: 'ingredients',
            Tag: 'tags'
        }
        model = Ingredient
        file_type = options['file_type']
        if options['tags']:
            model = Tag
        print(f'Импорт {model} из {filenames[model]}.{file_type} начался')
        filepath = f'{settings.BASE_DIR}/../data/{filenames[model]}.{file_type}'
        with open(filepath, 'r') as data_file:
            data = []
            if file_type == 'csv':
                data = csv.DictReader(data_file)
            else:
                print('json')
                data = json.load(data_file)
            model.objects.bulk_create(model(**t) for t in data)
        print(f'Данные из {filenames[model]}.{file_type} загружены')

    def add_arguments(self, parser):
        parser.add_argument(
            '-t',
            '--tags',
            action='store_true',
            default=False,
            help='Импорт тегов'
        )

        parser.add_argument(
            'file_type',
            nargs='?',
            choices=['json', 'csv'],
            default='json',
            help='Выбор типа ипрортируемого файла: csv или json'
        )

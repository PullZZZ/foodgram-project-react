import csv
import json
import logging

from django.conf import settings
from django.core.management.base import BaseCommand

from recipes.models import Ingredient, Tag


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s, %(levelname)s, %(message)s',
)

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    _settings = {
        'model': Ingredient,
        'dir': f'{settings.BASE_DIR}/data/',
        'file': 'ingredients',
    }

    def handle(self, *args, **options):
        if options['tags']:
            self._settings['model'] = Tag
            self._settings['file'] = 'tags'
        if options['file']:
            filepath = options['file']
        else:
            filepath = (f"{self._settings['dir']}"
                        f"{self._settings['file']}."
                        f"{options['file_type']}")

        self._import_data(self._settings['model'],
                          filepath, options['file_type'])

    def add_arguments(self, parser):
        parser.add_argument(
            '-f',
            '--file',
            type=str,
            help='Путь до файла с данными'
        )
        parser.add_argument(
            '-t',
            '--tags',
            action='store_true',
            default=False,
            help='Импорт тегов'
        )

        parser.add_argument(
            '--file_type',
            nargs='?',
            choices=['json', 'csv'],
            default='json',
            help=('Выбор типа ипрортируемого файла: csv или json'
                  '(по умолчанию json)')
        )

    def _import_data(self, model, filepath, file_type):
        logger.info(f'Импорт {filepath} начался')
        try:
            with open(filepath, 'r') as data_file:
                data = []
                if file_type == 'csv':
                    data = csv.DictReader(data_file)
                else:
                    data = json.load(data_file)
                model.objects.bulk_create(model(**line) for line in data)
            logger.info(f'Данные из {filepath} загружены')
        except Exception as error:
            logger.error(error)

import re
from django.core.management.base import BaseCommand
from boards.models import Boards

class Command(BaseCommand):
    help = '把奇怪的資料都修光光'

    def handle(self, *args, **options):
        alias_cities = {
            '台北': '台北市',
            '新北': '新北市'
        }
        for alias in alias_cities:
            boards = Boards.objects.filter(county=alias)
            count = 0
            for board in boards:
                board.county = alias_cities[alias]
                board.save()
                count += 1

            self.stdout.write('把 {} 筆 {} 改成 {}'.format(count, alias, alias_cities[alias]))

        alias_districtss = {
            '台北市': {
                '北投': '北投區'
            }
        }

        # do later, looks like to be systematic error


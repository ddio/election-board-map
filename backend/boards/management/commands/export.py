import json
from os import path
from django.core.management.base import BaseCommand
from boards.models import Boards
from candidates.models import Terms

class Command(BaseCommand):
    help = '把想要的資料會出成 JSON'
    export_dir = path.join(path.dirname(path.realpath(__file__)), '../../../../datas')

    def handle(self, *args, **options):
        # 匯出所有資料，無論有無查核過
        # 匯出的東西放在 datas/boards.json, datas/candidates.json

        board_dict = {}
        board_fields = {
            'id': True,
            'image': lambda x: path.basename(x),
            'coordinates': lambda x: x.coords,
            'county': True,
            'district': True,
            'road': True,
            'verified_amount': True,
            'candidates': lambda candidates: list(map(lambda cand: cand.id, candidates.all()))
        }
        for board in Boards.objects.all():
            detail = {}
            for field in board_fields:
                value = getattr(board, field)
                if board_fields[field] is True:
                    detail[field] = value
                else:
                    detail[field] = board_fields[field](value)

            board_dict[board.id] = detail

        with open(path.join(self.export_dir, 'boards.json'), 'w') as outfile:
            json.dump(board_dict, outfile)


import json
from os import path
from django.core.management.base import BaseCommand
from boards.models import Boards
from candidates.models import Terms

class Command(BaseCommand):
    help = '把想要的資料會出成 JSON'
    export_dir = path.join(path.dirname(path.realpath(__file__)), '../../../../datas')

    def dump_it(self, queryset, formatter):
        ret = {}
        for row in queryset:
            detail = {}
            for field in formatter:
                value = getattr(row, field)
                if formatter[field] is True:
                    detail[field] = value
                else:
                    detail[field] = formatter[field](value)

            ret[row.pk] = detail

        return ret

    def export_boards(self):
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
        board_dict = self.dump_it(Boards.objects.all(), board_fields)

        self.stdout.write('Export {} boards'.format(len(board_dict)))
        with open(path.join(self.export_dir, 'boards.json'), 'w') as outfile:
            json.dump(board_dict, outfile, ensure_ascii=False)

    def export_candidates(self):
        formatter = {
            'id': True,
            'number': True,
            'name': True,
            'party': True,
            'county': True,
            'district': True,
            'image': True,
            'candidate': lambda x: x.id,
            'type': True,
            'boards_set': lambda boards: list(map(lambda board: board.id, boards.all()))
        }
        candidates = self.dump_it(
            Terms.objects.filter(election_year='2018'),
            formatter
        )
        routes = []
        for candidate_id in candidates:
            route_prefix = '/2018/{}-{}'.format(candidates[candidate_id]['name'], candidate_id)
            if not candidates[candidate_id]['boards_set']:
                routes.append(route_prefix)

            for board_id in candidates[candidate_id]['boards_set']:
                routes.append('{}/{}'.format(route_prefix, board_id))

        self.stdout.write('Export {} candidates'.format(len(candidates)))
        with open(path.join(self.export_dir, 'candidates.json'), 'w') as outfile:
            json.dump(candidates, outfile, ensure_ascii=False)

        self.stdout.write('Export {} routes'.format(len(routes)))
        with open(path.join(self.export_dir, 'routes.json'), 'w') as outfile:
            json.dump(routes, outfile, ensure_ascii=False)

    def handle(self, *args, **options):
        # 匯出所有資料，無論有無查核過
        # 匯出的東西放在 datas/boards.json, datas/candidates.json

        self.export_boards()
        self.export_candidates()


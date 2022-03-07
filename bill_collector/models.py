import django
from django.db import models
from common.utils import query_string_to_dict, logger


class Invoice(models.Model):
    date = models.DateTimeField()
    bank_name = models.CharField(max_length=30)
    number = models.FloatField()
    direction = models.CharField(max_length=10)
    ivc_type = models.CharField(max_length=30)
    ivc_comment = models.CharField(max_length=300)

    def __str__(self):
        if self.direction == 'income':
            ivc_direction = '+'
        else:
            ivc_direction = '-'

        return '({}) {}${} for {}'.format(self.id, ivc_direction, self.number, self.ivc_type)

    def __repr__(self):
        if self.direction == 'income':
            ivc_direction = '+'
        else:
            ivc_direction = '-'

        return 'IVC{}: {}${}/{}/{}/{}'.format(self.id, ivc_direction, self.number, self.bank_name, self.ivc_type,
                                              self.date)

    @classmethod
    def get_ivc_for_monthly_bill(cls, year: str, month: str) -> django.db.models.query.QuerySet:
        year, month = str(year), str(month)
        return cls.objects.filter(date__year=year, date__month=month)

    @classmethod
    def get_info_for_monthly_bill(cls, year: str, month: str) -> dict:
        """
        helper method to generate bill dict whose keys are banks
        return dict:

        {
            'bank_1': [ivc1, ivc2, ...],
            'bank_2': [ivc1, ivc2, ...],
            'bank_3': [ivc1, ivc2, ...],
            ...
        }
        """
        ivcs = cls.get_ivc_for_monthly_bill(year, month)
        info = dict()
        for ivc in ivcs:
            info.setdefault(ivc.bank_name, []).append(ivc)

        return info

    @staticmethod
    def convert_bill_info_dict_to_2d_array(bill_info: dict) -> list:
        """
        helper method to generate bill table for frontend to render

        {                                                [
            'bank_1': [ivc(day1), i(d15), i(d30)],                [bank_1, bank_2, bank_3],
            'bank_2': [ivc(day5), i(d5), i(d20)],     >           [{i(d1)}, {}, {}         ],
            'bank_3': [ivc(day8), i(d18), i(d28)]                 ...
                                                                  [{}, {i(d5), i(d5)}, {}],
                                                                  ...
                                                                  [{}, {}, {i(d8)}],
                                                                  ...
                                                                  [{i(d15)}, {}, {}],
                                                                  ...
                                                                  [{}, {}, {i(d18)}],
                                                                  ...
                                                                  [{}, {i(d20)}, {}],
                                                                  ...
                                                                  [{}, {}, {i(d28)}],
                                                                  ...
                                                                  [{i(d30)}, {}, {}],
                                                                  []
        }                                                   ]
        """
        banks = [bk for bk in bill_info.keys()]
        bill_table = list()
        bill_table.append(banks)
        for _ in range(31):
            bill_table.append([set() for _ in range(len(banks))])

        for bk, ivcs in bill_info.items():
            col_idx = banks.index(bk)
            for ivc in ivcs:
                row_idx = ivc.date.day
                bill_table[row_idx][col_idx].add(ivc)

        return bill_table

    @staticmethod
    def bill_info_summary(bill_info: dict) -> dict:
        """
        helper method to classify invoices for frontend to render

        {                                                {
            'bank_1': [ivc1, i2, i3],                       'outcome': {
            'bank_2': [ivc1, i2, i3],     >                     'type1': xxx,
            'bank_3': [ivc1, i2, i3],                           'type2': xxx,
            ...                                                 ...,
        }                                                       'total': xxx
                                                            },
                                                            'income': {
                                                                'type1': xxx,
                                                                'type2': xxx,
                                                                ...,
                                                                'total': xxx
                                                            },
                                                            'total': xxx
                                                        }
        """
        bill_summary = {'outcome': {}, 'income': {}, 'total': 0}
        if not bill_info:
            logger.warn('empty bill info dict')
            return bill_summary

        for ivcs in bill_info.values():
            for ivc in ivcs:
                if ivc.direction == 'outcome':
                    bill_summary['outcome'][ivc.ivc_type] = bill_summary['outcome'].get(ivc.ivc_type, 0) + ivc.number
                    bill_summary['outcome']['total'] = bill_summary['outcome'].get('total', 0) + ivc.number
                else:
                    bill_summary['income'][ivc.ivc_type] = bill_summary['income'].get(ivc.ivc_type, 0) + ivc.number
                    bill_summary['income']['total'] = bill_summary['income'].get('total', 0) + ivc.number
        bill_summary['total'] = bill_summary['income'].get('total', 0) - bill_summary['outcome'].get('total', 0)
        return bill_summary

    @staticmethod
    def decorate_data_for_add_ivc(data) -> dict:
        if isinstance(data, str):
            data = query_string_to_dict(data)

        for k, v in data.items():
            if k in {'date', 'number', 'direction'}:
                continue

            if isinstance(v, str):
                v = v.strip(' +')
                v = v.replace(' ', '_')
                v = v.replace('+', '_')

            data.update({k: v})

        return data










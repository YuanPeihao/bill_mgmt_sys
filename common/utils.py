from calendar import monthrange
import logging


logger = logging.getLogger('bill_mgmt_sys')


def get_num_of_days_by_month(year: int, month: int) -> int:
    return monthrange(year, month)[1]


def query_string_to_dict(query: str) -> dict:
    pairs = query.split('&')
    res = dict()
    for pair in pairs:
        k, v = pair.split('=')
        res.update({k: v})
    return res


if __name__ == '__main__':
    print(get_num_of_days_by_month(2021, 3))
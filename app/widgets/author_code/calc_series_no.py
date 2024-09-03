import re


def calc_series_no(series_number):
    compiler = re.compile('[0-9]+')
    if not series_number:
        sn = 0
    else:
        sn = 0
        n = compiler.findall(series_number)
        i = 4
        for num in n:
            sn += int(num) * 10 ** i
            i = i - 2
            if i < 0:
                break
        if "S" in series_number:
            if series_number.startswith("S"):
                sn = sn + 10 ** 6
            else:
                sn = sn + 9000

    return sn


def calc_work_no(work_number):
    compiler = re.compile('[0-9]+')
    wn = compiler.findall(work_number)

    return int(wn[0])

from author_code.models import CutterSanbornThreeFigureAuthorTable
from widgets.author_code import normalization


def query(keyword):

    key = normalization.normalization(keyword)

    Table = CutterSanbornThreeFigureAuthorTable.objects.filter(pk__istartswith=key[0]).values_list('AuthorSymbol', 'AuthorName', flat=False).order_by('-pk')
    Table = list(Table)

    if key.startswith('mc'):
        key = 'mac' + key[2:]
    elif key.startswith('st '):
        key = 'saint' + key[2:]

    cutter = ""

    for Symbol, Name in Table:
        name = normalization.normalization(Name)
        if len(key) > len(name):
            skey = key[:len(name)]
        else:
            skey = key

        if skey >= name:
            cutter = Symbol
            break
        else:
            continue

    try:
        CutterSanborn = CutterSanbornThreeFigureAuthorTable.objects.get(pk=cutter)
    except CutterSanbornThreeFigureAuthorTable.DoesNotExist:
        CutterSanborn = None

    return CutterSanborn


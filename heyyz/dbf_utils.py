import heyy
import dbfread

pt = heyy.pathtool


def dbf2objs(filename, encoding='gbk', ignore_case=True):
    dbf = dbfread.DBF(filename, encoding)
    objs = [heyy.json2obj(r, ignore_case=ignore_case) for r in dbf.records]
    dbf.unload()
    return objs


def str2objs(attrs, string, *, sep='\t', newline='\n'):
    rows = string.split(newline)
    if isinstance(attrs, bool):
        head = rows[0]
        rows = rows[1:]
    else:
        head = attrs
    return [heyy.json2obj(dict(zip(head, s.split(sep)))) for s in rows]


def read_fields(dbf_filename, encoding='gbk'):
    dbf = dbfread.DBF(dbf_filename, encoding)
    return dbf.field_names


def split_multiline(string):
    return list(filter(None, string.split('\n')))


def compare_fields(fields_from, fields_to):
    f_order = {v.upper(): i for i, v in enumerate(fields_from)}
    t_order = {v.upper(): i for i, v in enumerate(fields_to)}
    ff = set(s.upper() for s in fields_from)
    ft = set(s.upper() for s in fields_to)
    f_unique = sorted(ff - ft, key=lambda attr: f_order.get(attr))
    t_unique = sorted(ft - ff, key=lambda attr: t_order.get(attr))
    share = sorted(ff & ft, key=lambda attr: (t_order.get(attr), f_order.get(attr)))
    print(f'来源表独特字段为：{f_unique}')
    print(f'目标表独特字段为：{t_unique}')
    print(f'两表共享的字段为：{share}')

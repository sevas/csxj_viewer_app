import version
import csxj.db as csxjdb
import version


def load_last_update_data(db_root):
    last_update = csxjdb.get_last_status_update(db_root)
    res = {}
    res.update(last_update)
    return res


def load_sidebar_data(db_root):
    overall_stats = csxjdb.get_overall_statistics(db_root)
    last_update = load_last_update_data(db_root)

    res = {}
    res.update(overall_stats)
    res.update(last_update)
    return res


def load_footer_data():
    return dict(version=version.VERSION)



def load_all_common_values(db_root):
    values = dict()
    values.update(load_sidebar_data(db_root))
    values.update(load_footer_data())
    return values

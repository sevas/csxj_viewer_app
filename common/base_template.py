import csxj.db as csxjdb
import csxj
import version




def load_last_update_data(db_root):
    last_update = csxjdb.get_statistics_from_last_update_for_all_sources(db_root)
    return last_update


def load_sidebar_data(db_root):
    total_metainfo = csxjdb.get_summed_statistics_for_all_sources(db_root)

    first_day, last_day = csxjdb.get_first_and_last_date(db_root)

    res = {}

    res.update({
        'start_date': first_day,
        'end_date':last_day,
        'num_providers':len(csxjdb.get_all_provider_names(db_root)),
    })

    res.update(total_metainfo)

    return res



def load_queued_items_count(db_root):
    sources = csxjdb.get_all_provider_names(db_root)
    queued_items_count = 0
    for source_name in sources:
        p = csxjdb.Provider(db_root, source_name)
        queued_items_count += p.get_queued_items_count()

    return {'queued_items_count':queued_items_count}


def load_footer_data():
    return dict(version=version.VERSION, csxj_version=csxj.__version__)



def load_all_common_values(db_root):
    values = dict()
    values.update(load_sidebar_data(db_root))
    values.update(load_footer_data())
    values.update(load_queued_items_count(db_root))
    values['last_update'] = load_last_update_data(db_root)
    return values

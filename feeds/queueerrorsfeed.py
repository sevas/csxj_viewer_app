from django.contrib.syndication.views import Feed
import os.path
import csxj.db as csxjdb


STATIC_DATA_PATH = os.path.join(os.path.dirname(__file__), '../static_data')


def flatten_error_dict(all_errors):
    flattened_list = list()

    for name, error_dict in all_errors:
        for date, errors in error_dict.items():
            for hour, trace in errors.items():
                flattened_list.append((date, hour, name, trace))

    def comp_error_items(e1, e2):
        # wtf is that shit?!
        if e1[0] < e2[0]:
            return -1
        elif e1[0] == e2[0]:
            if e1[1] == e2[1]: return -1
            elif e1[1] == e2[1]: return 0
            else: return 1
        else:
            return 1

    flattened_list.sort(cmp=comp_error_items)

    return flattened_list



class LatestEntriesFeed(Feed):
    title = "csxj crawler queue errors feed"
    link = "http://tartiflette.ulb.ac.be:8081"
    description = ""

    def items(self):
        return flatten_error_dict(csxjdb.get_queue_errors_for_all_sources(STATIC_DATA_PATH))


    def item_title(self, item):
        return "[On {0} at {1}] New queue error for {2}".format(*item)


    def item_description(self, item):
        return item[3]


    def item_link(self, item):
        return "{0}/source/{1}/queue".format(self.link, item[2])




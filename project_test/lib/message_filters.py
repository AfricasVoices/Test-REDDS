from dateutil.parser import isoparse

class MessageFilters(object):
    @staticmethod
    def filter_test_messages(messages, test_run_key="test_run"):
        return [td for td in messages if not td.get(test_run_key, False)]
    
    @staticmethod
    def filter_empty_messages(messages, messages_keys):
        #Before using in future projects, consider whether messages which are "" should be considerd as empty
        non_empty = []
        for td in messages:
            for messages_key in messages_keys:
                if messages_key in td:
                    non_empty.append(td)
                    continue
        return non_empty

    @staticmethod
    def filter_time_range(messages, time_key, starts_time, end_time):
        return [td for td in messages if starts_time <= isoparse(td.get(time_key)) <= end_time]

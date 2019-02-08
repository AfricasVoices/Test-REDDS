from dateutil.parser import isoparse

class MessageFilters(object):

    @staticmethod
    def filter_test_messages(messages, test_run_key="test_run"):
        return [td for td in messages if not td.get(test_run_key, False)]
    
    @staticmethod
    def filter_empty_messages  (messages, messages_keys):

        non_empty = []
        for td in messages:
            for message_key in message_keys:
                if message_key in td:
                    non_empty.append(td)
                    continue
        return non_empty
    @staticmethod
    def filter_time_range(message, time_key, start_time, end_time):
        return [td for td in messages if start_time <= isoparse(td.get(time_key)) <= end_time]

    @staticmethod
    def filter_noise(messages, message_key, noise_fn):
        return [td for in messages if not noise_fn(td.get(message_key))]
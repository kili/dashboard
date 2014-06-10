from user_billing.metering.ceilometer import data_fetcher


class RawDataFetcher(object):

    has_more_data = 1

    def __init__(self):
        self.data_source = data_fetcher.CeilometerDataFetcher('instance')

    def fetch(self, timespan=3600):
        for data_chunk in self.data_source:
            print "one chunk"
            print(data_chunk)
            self.data_source.confirm_data_is_received()

class DisplayConverter:

    conversions = {
        'ki': 1024,
        'Mi': 1024 * 1024,
        'Gi': 1024 * 1024 * 1024
    }

    def __init__(self, to=None):
        self._to = to

    @property
    def divisor(self) -> int:
        """
        Gets divsor based on string key
        :return: int value of divisor
        """
        if self._to:
            try:
                self.conversions[self._to]
            except KeyError:
                raise ValueError('must convert to one of: ki, Mi, Gi')
            else:
                return self.conversions[self._to]
        else:
            return 1

    def convert(self, data_bytes: int) -> float:
        """
        converts number based on divisor
        :param data_bytes: byte number to convert
        :return: converted bytes
        """
        return data_bytes / self.divisor

    def get(self) -> int:
        """
        gets divisor
        """
        return self.divisor
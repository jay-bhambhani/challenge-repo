import typing
from datetime import datetime

from src.abstractions.display_converter import DisplayConverter


class S3SimpleDist:
    """
    Abstraction so represent distributions of file sizes
    """

    def __init__(self):
        self.mi = DisplayConverter('Mi').get()
        self._zero_to_one = 0
        self._one_to_ten = 0
        self._ten_to_hundred = 0
        self._hundred_to_gig = 0
        self._gig_to_5 = 0
        self._five_plus_gigs = 0

    def add(self, size: int):
        """
        add a size to distribution
        :param size: file size to add
        """
        if size < self.mi:
            self._zero_to_one += 1
        elif self.mi <= size < 10 * self.mi:
            self._one_to_ten += 1
        elif 10 * self.mi <= size < 100 * self.mi:
            self._ten_to_hundred += 1
        elif 100 * self.mi <= size < self.mi * 1024:
            self._hundred_to_gig += 1
        elif self.mi * 1024 <= size < 5 * self.mi * 1024:
            self._gig_to_5 += 1
        else:
            self._five_plus_gigs += 1

    def header(self) -> typing.Sequence[str]:
        """
        NOTE: janky - easiest way to convert properties to the output table header
        :return:
        """
        return ['0-1Mi', '1-10Mi', '10-100Mi', '100Mi-1Gi', '1-5Gi', '5Gi+']

    def to_list(self) -> typing.Sequence[int]:
        """
        NOTE: janky easiest way to convert property values to output row
        :return:
        """
        return [self._zero_to_one, self._one_to_ten, self._ten_to_hundred, self._hundred_to_gig, self._gig_to_5, self._five_plus_gigs]

class BucketStats:
    """
    Abstraction layer for bucket statistics
    """

    def __init__(self, name: str, creation_date: datetime, last_modified: datetime):
        self.name = name
        self.creation_date = creation_date
        self.last_modified = last_modified
        self._size_distributions = S3SimpleDist()
        self._props =  ['name', 'creation_date', 'last_modified', 'number_of_files', 'total_file_size']
        self.number_of_files = 0
        self.total_file_size = 0

    def update(self, obj):
        """
        update bucket statistics with object data
        :param obj: s3.Object
        """
        self._update_last_modified(obj.last_modified)
        self._update_file_data(obj.size)

    def _update_last_modified(self, last_modified):
        """
        update internal last modified with new obj last modified
        :param last_modified: datetime of new last modified object
        """
        if self.last_modified < last_modified:
            self.last_modified = last_modified

    def _update_file_data(self, content_length):
        """
        update file numbers based on new object data
        :param content_length: size of s3.Object
        """
        self.number_of_files += 1
        self.total_file_size += content_length
        self._size_distributions.add(content_length)

    @property
    def fields(self) -> typing.Sequence[str]:
        """
        get bucket stats fields: NOTE - janky
        :return:
        """
        for key in self._props + self._size_distributions.header():
            yield key

    @property
    def props(self):
        """
        get bucket stats props: NOTE - janky
        :return:
        """
        for value in [getattr(self, key) for key in self._props] + self._size_distributions.to_list():
            yield value

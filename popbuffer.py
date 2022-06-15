import random


class PopBuffer:
    def __init__(self, size, reverse=False, key=None):
        self._key = key
        self._list = []
        self.size = size
        self.reverse = reverse

    def append(self, data):
        self._list.append(data)
        self._list.sort(key=self._key, reverse=self.reverse)
        if len(self._list) > self.size:
            self._list.pop(-1)
        
        
    def random_choice(self):
        #print(self._list)
        return random.choice(self._list)


    def best(self, k):
        self._list.sort(key=self._key, reverse=self.reverse)
        return self._list[:k]


    def __getitem__(self, key):
        return self._list[key]



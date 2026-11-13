class TransactionIterator:
    def __init__(self, transactions: list, category_filter: str = None):
        self._transactions = transactions
        self._category_filter = category_filter
        self._index = 0

    def __iter__(self):
        return self

    def __next__(self):
        while self._index < len(self._transactions):
            trx = self._transactions[self._index]
            self._index += 1
            if not self._category_filter or trx.get_details()["category"] == self._category_filter:
                return trx
        raise StopIteration
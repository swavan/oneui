from PyQt5.QtCore import QAbstractTableModel, Qt


class SwaVanHeader(QAbstractTableModel):
    def __init__(self, data):
        super(SwaVanHeader, self).__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            super().data(index, role)
            return self._data[index.row()][index.column()]

    def rowCount(self, index):
        # The length of the outer list.
        super().rowCount(index)
        return len(self._data)

    def columnCount(self, index):
        # The following takes the first sub-list, and returns
        # the length (only works if all rows are an equal length)
        super().columnCount(index)
        return len(self._data[0])

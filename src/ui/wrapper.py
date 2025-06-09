from PyQt5.QtWidgets import QStyledItemDelegate
from PyQt5.QtCore import Qt, QSize

class Wrapper(QStyledItemDelegate):
    def paint(self, painter, option, index):
        option.displayAlignment = Qt.AlignLeft | Qt.AlignVCenter
        super().paint(painter, option, index)

    def sizeHint(self, option, index):
        text = index.data()
        metrics = option.fontMetrics
        rect = metrics.boundingRect(0, 0, option.rect.width(), 0, Qt.TextWordWrap, text)
        return QSize(option.rect.width(), rect.height() + 10)
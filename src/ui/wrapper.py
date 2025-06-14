from PyQt5.QtWidgets import QStyledItemDelegate, QStyleOptionViewItem
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QTextOption, QTextDocument, QPainter

class Wrapper(QStyledItemDelegate):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._cached_sizes = {} # Cache for item sizes

    def paint(self, painter: QPainter, option: QStyleOptionViewItem, index):
        # Your existing painting logic
        text = index.data(Qt.DisplayRole)
        if not text:
            return

        doc = QTextDocument()
        doc.setDefaultFont(option.font)
        doc.setTextWidth(option.rect.width()) # Set text width to current item width for wrapping
        doc.setHtml(text) # Or setText(text) if not rich text

        painter.save()
        painter.translate(option.rect.topLeft())
        doc.drawContents(painter)
        painter.restore()

    def sizeHint(self, option: QStyleOptionViewItem, index):
        text = index.data(Qt.DisplayRole)
        if not text:
            return QSize(0, 0)

        # Use a unique key for caching (e.g., index.row() and text content)
        cache_key = (index.row(), text)
        if cache_key in self._cached_sizes:
            return self._cached_sizes[cache_key]

        doc = QTextDocument()
        doc.setDefaultFont(option.font)
        doc.setTextWidth(option.rect.width()) # Crucial for accurate height calculation
        doc.setHtml(text) # Or setText(text)

        # Calculate the required height
        height = int(doc.size().height())
        
        # Cache the size
        self._cached_sizes[cache_key] = QSize(option.rect.width(), height)
        return self._cached_sizes[cache_key]

    def clear_cache(self):
        self._cached_sizes.clear()
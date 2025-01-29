"""
Custom Widgets for Interefaces

Author: Brandon Bauer
Written January 25

Updated XXXXXXXXXXXX
"""

from PyQt6.QtGui import QColor, QPalette, QPainter
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QLineEdit


class Color(QWidget):
    def __init__(self, color):
        super().__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(color))
        self.setPalette(palette)
        
class CustomLineEdit(QLineEdit):
    def __init__(self, background_text, parent=None):
        super().__init__(parent)
        self.background_text = background_text  # Permanent text
        self.setAlignment(Qt.AlignmentFlag.AlignLeft)  # Align user input to the right

    def paintEvent(self, event):
        """Custom paint event to draw the permanent background text."""
        super().paintEvent(event)

        # Draw permanent background text
        painter = QPainter(self)
        painter.setPen(QColor("white"))  # Set color for the background text
        font_metrics = painter.fontMetrics()
        
        # Calculate position for the permanent text
        text_width = font_metrics.horizontalAdvance(self.background_text)
        y_position = (self.height() + font_metrics.ascent() - font_metrics.descent()) // 2
        x_position = self.width() - text_width - 5  # Right-align the text with a margin
        
        # Draw the text
        painter.drawText(x_position, y_position, self.background_text)
        painter.end()

    def textChangedEvent(self):
        """Disable deletion of the permanent text (optional, not needed with custom paint)."""
        pass

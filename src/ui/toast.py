from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt, QPropertyAnimation, QTimer, QPoint, pyqtSignal
from PyQt5.QtGui import QFont

class ToastManager:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.active_toasts = []
            cls._instance.toast_spacing = -15  # Space between toasts
        return cls._instance
    
    def add_toast(self, toast):
        self.active_toasts.append(toast)
        self._position_toast(toast)
    
    def remove_toast(self, toast):
        if toast in self.active_toasts:
            self.active_toasts.remove(toast)
            self._reposition_all_toasts()
    
    def _position_toast(self, new_toast):
        if len(self.active_toasts) == 1:
            # First
            new_toast.move(new_toast.target_x, new_toast.base_y)
        else:
            lowest_y = new_toast.base_y
            for toast in self.active_toasts[:-1]:
                if toast.isVisible():
                    toast_bottom = toast.y() + toast.height()
                    if toast_bottom > lowest_y:
                        lowest_y = toast_bottom
            
            # Position new toast below
            new_y = lowest_y + self.toast_spacing
            new_toast.move(new_toast.target_x, new_y)
    
    def _reposition_all_toasts(self):
        current_y = None
        for toast in self.active_toasts:
            if toast.isVisible():
                if current_y is None:
                    # First goes to base
                    current_y = toast.base_y
                    toast.move(toast.target_x, current_y)
                else:
                    current_y = current_y + toast.height() + self.toast_spacing
                    toast.move(toast.target_x, current_y)

class Toast(QWidget):
    closing = pyqtSignal()
    
    def __init__(self, message, duration=3000, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_DeleteOnClose)
        
        self.setStyleSheet("""
            QWidget {
                background-color: rgba(255, 200, 0, 220);
                color: black;
                border-radius: 10px;
                font-size: 14px;
                font-weight: bold;
            }
        """)

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 15, 20, 15)
        
        label = QLabel(message)
        label.setAlignment(Qt.AlignCenter)
        label.setWordWrap(True)
        layout.addWidget(label)
        
        self.setLayout(layout)
        
        self.setFixedWidth(250)
        self.adjustSize()

        self.manager = ToastManager()
        self.base_y = 0
        self.target_x = 0
        
        # Animations
        self.fade_in_animation = QPropertyAnimation(self, b"windowOpacity")
        self.fade_in_animation.setDuration(300)
        self.fade_in_animation.setStartValue(0.0)
        self.fade_in_animation.setEndValue(0.95)
        
        self.fade_out_animation = QPropertyAnimation(self, b"windowOpacity")
        self.fade_out_animation.setDuration(300)
        self.fade_out_animation.setStartValue(0.95)
        self.fade_out_animation.setEndValue(0.0)
        self.fade_out_animation.finished.connect(self._force_close)
        
        # Timer
        self.auto_close_timer = QTimer()
        self.auto_close_timer.setSingleShot(True)
        self.auto_close_timer.timeout.connect(self.start_fade_out)
        self.duration = duration

    def show_above(self, parent_widget):
        if not parent_widget:
            return
            
        parent_pos = parent_widget.mapToGlobal(QPoint(0, 0))
        self.target_x = parent_pos.x() + (parent_widget.width() - self.width()) // 2
        self.base_y = parent_pos.y() + 10
        
        self.show()
        self.raise_()
        
        self.manager.add_toast(self)
        
        self.setWindowOpacity(0.0)
        self.fade_in_animation.start()
        
        # Start timer
        if self.duration > 0:
            self.auto_close_timer.start(self.duration)

    def start_fade_out(self):
        self.auto_close_timer.stop()
        self.fade_out_animation.start()

    def _force_close(self):
        self.closing.emit()
        self.close()

    def closeEvent(self, event):
        if hasattr(self, 'auto_close_timer'):
            self.auto_close_timer.stop()
        if hasattr(self, 'fade_in_animation'):
            self.fade_in_animation.stop()
        if hasattr(self, 'fade_out_animation'):
            self.fade_out_animation.stop()
            
        if hasattr(self, 'manager'):
            self.manager.remove_toast(self)
            
        super().closeEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.start_fade_out()
        super().mousePressEvent(event)

# TESTING FUNCTIONS
def show_toast(parent_widget, message, duration=3000):
    toast = Toast(message, duration, parent_widget)
    toast.show_above(parent_widget)
    return toast

def test_toasts(parent_widget):
    messages = [
        "First toast message",
        "Second toast - should be below first",
        "Third toast - should be at bottom",
        "Fourth toast - stacking test"
    ]
    
    for i, msg in enumerate(messages):
        QTimer.singleShot(i * 200, lambda m=msg: show_toast(parent_widget, m, 5000))

if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    
    app = QApplication(sys.argv)
    
    # Create a test parent widget
    parent_widget = QWidget()
    parent_widget.resize(400, 300)
    parent_widget.setWindowTitle("Toast Test")
    parent_widget.show()
    
    test_toasts(parent_widget)
    
    sys.exit(app.exec_())
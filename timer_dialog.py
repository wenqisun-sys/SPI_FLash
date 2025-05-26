from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtWidgets import QDialog, QLabel, QVBoxLayout

class TimerDialog(QDialog):
    def __init__(self, parent, duration_hours):
        super().__init__(parent)
        self.setWindowTitle("Test in Progress")
        self.setModal(False)  # 非模态
        self.setStyleSheet("background-color: #1E293B; border-radius: 10px;")  # 深灰背景，圆角

        # 支持小数时间，转换为秒
        self.duration_seconds = int(float(duration_hours) * 3600)  # 小时转秒，支持小数
        self.remaining_seconds = self.duration_seconds

        layout = QVBoxLayout()
        # 时间标签，电子时钟样式
        self.label = QLabel(self.format_time(self.remaining_seconds))
        self.label.setStyleSheet("""
            font-size: 48px; 
            color: #10B981; 
            font-weight: bold; 
            font-family: 'Courier New', monospace; 
            padding: 20px; 
            background-color: #1F2A44; 
            border: 2px solid #10B981; 
            border-radius: 5px; 
            qproperty-alignment: AlignCenter;
        """)
        layout.addWidget(self.label, alignment=Qt.AlignCenter)

        self.setLayout(layout)
        self.setFixedSize(350, 200)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)
        self.timer.start(1000)  # 每秒更新

    def format_time(self, seconds):
        """格式化时间为 HH:MM:SS"""
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        secs = seconds % 60
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"

    def update_timer(self):
        if self.remaining_seconds > 0:
            self.remaining_seconds -= 1
            self.label.setText(self.format_time(self.remaining_seconds))
        else:
            self.timer.stop()
            self.accept()  # 关闭对话框

    def closeEvent(self, event):
        self.timer.stop()
        super().closeEvent(event)
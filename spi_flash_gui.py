import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTextEdit, QComboBox, QLabel, QLineEdit
from PyQt5.QtCore import Qt
from commands import CommandHandler

class SpiFlashGui(QMainWindow):
    def __init__(self):
        super().__init__()
        # 先初始化 command_handler
        self.command_handler = CommandHandler(self)
        # 再调用 initUI
        self.initUI()

    def initUI(self):
        self.setWindowTitle("SPI Flash 操作界面")
        self.setGeometry(100, 100, 800, 600)

        # 主布局
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)

        # 左侧按钮区域
        button_widget = QWidget()
        button_layout = QVBoxLayout(button_widget)
        button_layout.setAlignment(Qt.AlignTop)

        # 基本操作组
        basic_group = QWidget()
        basic_layout = QHBoxLayout(basic_group)
        self.open_button = QPushButton("打开串口")
        self.open_button.setStyleSheet("background-color: #00FF00; color: white; padding: 10px;")
        self.close_button = QPushButton("关闭串口")
        self.close_button.setStyleSheet("background-color: #FF0000; color: white; padding: 10px;")
        basic_layout.addWidget(self.open_button)
        basic_layout.addWidget(self.close_button)
        button_layout.addWidget(basic_group)

        # 串口选择
        port_label = QLabel("串口选择:")
        self.port_combo = QComboBox()
        self.port_combo.addItem("请选择串口")  # 添加默认提示
        port_layout = QHBoxLayout()
        port_layout.addWidget(port_label)
        port_layout.addWidget(self.port_combo)
        button_layout.addLayout(port_layout)

        # 读 ID 按钮
        self.read_id_button = QPushButton("读 ID")
        self.read_id_button.setStyleSheet("background-color: #00FF00; color: white; padding: 10px;")
        button_layout.addWidget(self.read_id_button)

        # 擦除按钮
        self.erase_button = QPushButton("擦除")
        self.erase_button.setStyleSheet("background-color: #FF0000; color: white; padding: 10px;")
        button_layout.addWidget(self.erase_button)

        # 坏块扫描按钮
        self.badblock_button = QPushButton("坏块扫描")
        self.badblock_button.setStyleSheet("background-color: #0000FF; color: white; padding: 10px;")
        button_layout.addWidget(self.badblock_button)

        # 新增：输入框和执行按钮
        command_input_layout = QHBoxLayout()
        self.command_input = QLineEdit()
        self.command_input.setPlaceholderText("输入指令，例如：eraseblockrange 0 10")
        self.execute_button = QPushButton("执行")
        self.execute_button.setStyleSheet("background-color: #FFA500; color: white; padding: 10px;")
        command_input_layout.addWidget(self.command_input)
        command_input_layout.addWidget(self.execute_button)
        button_layout.addLayout(command_input_layout)

        # 右侧显示区域
        self.display_text = QTextEdit()
        self.display_text.setReadOnly(True)
        self.display_text.setStyleSheet("background-color: #FFFFFF;")

        # 布局
        main_layout.addWidget(button_widget, 1)
        main_layout.addWidget(self.display_text, 3)

        # 连接信号
        self.open_button.clicked.connect(self.command_handler.open_serial)
        self.close_button.clicked.connect(self.command_handler.close_serial)
        self.read_id_button.clicked.connect(self.command_handler.read_flash_id)
        self.erase_button.clicked.connect(self.command_handler.erase_chip)
        self.badblock_button.clicked.connect(self.command_handler.badblock_scan)
        self.execute_button.clicked.connect(self.command_handler.execute_custom_command)

    def append_text(self, text):
        self.display_text.append(text)

    def set_open_button_text(self, text):
        self.open_button.setText(text)

    def update_com_ports(self, ports):
        self.port_combo.clear()
        self.port_combo.addItem("请选择串口")
        for port in ports:
            self.port_combo.addItem(port.device)
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QComboBox, QCheckBox,QPushButton, QTextEdit, QTabWidget, \
    QGridLayout, QLineEdit, QLabel, QHBoxLayout, QFrame, QStatusBar, QMessageBox, QFileDialog
from PyQt5.QtGui import QFont, QIcon, QPixmap, QColor
from PyQt5.QtCore import Qt
import sys
import os
import datetime
from timer_dialog import TimerDialog

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        # 打包后，从 sys._MEIPASS 加载
        full_path = os.path.join(sys._MEIPASS, relative_path)
    else:
        # 开发环境，从项目目录加载
        full_path = os.path.join(os.path.abspath("."), relative_path)
    print(f"Resource path: {full_path}")  # 调试路径
    return full_path

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("UMT FlashPro")
        self.setGeometry(100, 100, 700, 600)

        self.setWindowIcon(QIcon(resource_path("lightning.ico")))

        # 翻译字典
        self.translations = {
            "English": {
                "open_serial": "Open Serial",
                "close_serial": "Close Serial",
                "disconnected": "Disconnected",
                "clear": "Clear",
                "save_log": "Save Log",
                "tooltip_save_log": "Save log to file",
                "tab_basic_functions": "Basic Functions",
                "tab_pageread": "Page Read",
                "tab_page_range_ops": "Page Range Ops",
                "tab_erase": "Erase",
                "tab_burnin_test": "BurnIn test",
                "tab_pe_cycles_test": "P/E Cycles Test",
                "tooltip_select_port": "Select serial port",
                "tooltip_open_serial": "Open or close serial port connection",
                "tooltip_read_id": "Read NAND Flash ID",
                "tooltip_bad_block": "Scan for bad blocks",
                "tooltip_erase_chip": "Erase entire chip (Note: This operation is irreversible)",
                "tooltip_scan_chip_ecc": "Scan chip ECC status",
                "tooltip_erase_chip_skip": "Erase chip and skip bad blocks (Note: This operation is irreversible)",
                "tooltip_noptest": "Execute NOP Test",
                "tooltip_fullchiprandom": "Write random data to entire chip",
                "tooltip_setwp_high": "Set write protection to high",
                "tooltip_setwp_low": "Set write protection to low",
                "tooltip_sethold_high": "Set hold signal to high",
                "tooltip_sethold_low": "Set hold signal to low",
                "tooltip_page_address": "Enter page address in decimal",
                "tooltip_read_page": "Read data from specified page",
                "tooltip_otp_read": "Read OTP area data",
                "tooltip_start_page": "Enter start page address in decimal",
                "tooltip_end_page": "Enter end page address in decimal (optional)",
                "tooltip_write_page_range": "Write data to a page or page range",
                "tooltip_verify_page_range": "Verify data in a page or page range",
                "tooltip_rand_write_crc": "Write random data with CRC to page range",
                "tooltip_rand_verify_crc": "Verify random data with CRC in page range",
                "tooltip_block_address": "Enter block address in decimal",
                "tooltip_erase_block": "Erase specified block (Note: This operation is irreversible)",
                "tooltip_scan_block_ecc": "Scan ECC status for the specified block",
                "tooltip_clear_output": "Clear log output",
                "tooltip_data_type": "Enter data type, format: 0x followed by 4 hexadecimal digits (e.g., 0x5A5A)",
                "tooltip_interval_custom": "Enter interval between odd and even cycles in milliseconds (e.g., 1000 for 1 second)",
                "tooltip_chip_write": "Write specified data to chip",
                "tooltip_chip_verify": "Verify chip data integrity",
                "tooltip_block_address_random": "Enter block address in decimal",
                "tooltip_cycles_random": "Enter number of cycles (0 for infinite)",
                "tooltip_pe_abl": "Perform PE ABL test with specified block and cycles",
                "tooltip_pe_eobl": "Perform PE EOBL test with specified block and cycles",
                "tooltip_lifetime_random": "Perform lifetime test with random data",
                "tooltip_num_blocks": "Enter number of blocks to test (e.g., 3)",
                "tooltip_block_address_custom": "Enter block address in decimal",
                "tooltip_odd_data": "Enter odd page data, format: 0x followed by 4 hexadecimal digits (e.g., 0x55AA)",
                "tooltip_even_data": "Enter even page data, format: 0x followed by 4 hexadecimal digits (e.g., 0xAA55)",
                "tooltip_cycles_custom": "Enter number of cycles (0 for infinite)",
                "tooltip_lifetime_custom": "Perform lifetime test with custom data",
                "confirm_erase_chip_title": "Confirm Erase",
                "confirm_erase_chip_message": "Are you sure you want to erase the entire chip? This operation is irreversible!",
                "confirm_erase_chip_skip_title": "Confirm Erase",
                "confirm_erase_chip_skip_message": "Are you sure you want to erase the chip and skip bad blocks? This operation is irreversible!",
                "confirm_erase_block_title": "Confirm Erase",
                "confirm_erase_block_message": "Are you sure you want to erase the specified block? This operation is irreversible!"
            },
            "Chinese": {
                "open_serial": "打开串口",
                "close_serial": "关闭串口",
                "disconnected": "未连接",
                "clear": "清除",
                "save_log": "保存日志",
                "tooltip_save_log": "将日志保存到文件",
                "tab_basic_functions": "闪存操作",
                "tab_pageread": "页面读取",
                "tab_page_range_ops": "页面范围操作",
                "tab_erase": "块擦除",
                "tooltip_scan_block_ecc": "扫描指定块的 ECC 状态",
                "tab_burnin_test": "老化测试",
                "tab_pe_cycles_test": "寿命测试",
                "tooltip_select_port": "选择串口设备",
                "tooltip_open_serial": "打开或关闭串口连接",
                "tooltip_read_id": "读取 NAND Flash 的 ID",
                "tooltip_bad_block": "扫描坏块",
                "tooltip_erase_chip": "擦除整个芯片（注意：此操作不可逆）",
                "tooltip_scan_chip_ecc": "扫描芯片 ECC 状态",
                "tooltip_erase_chip_skip": "擦除芯片并不跳过坏块（注意：此操作不可逆）",
                "tooltip_noptest": "执行 NOP 测试",
                "tooltip_fullchiprandom": "对整个芯片写入随机数据",
                "tooltip_setwp_high": "设置写保护为高电平",
                "tooltip_setwp_low": "设置写保护为低电平",
                "tooltip_sethold_high": "设置保持信号为高电平",
                "tooltip_sethold_low": "设置保持信号为低电平",
                "tooltip_page_address": "输入十进制的页面地址",
                "tooltip_read_page": "读取指定页面数据",
                "tooltip_otp_read": "读取 OTP 区域数据",
                "tooltip_start_page": "输入十进制的起始页面地址",
                "tooltip_end_page": "输入十进制的结束页面地址（可选）",
                "tooltip_write_page_range": "向页面或页面范围写入数据",
                "tooltip_verify_page_range": "验证页面或页面范围内的数据",
                "tooltip_rand_write_crc": "向页面范围写入带 CRC 的随机数据",
                "tooltip_rand_verify_crc": "验证页面范围内的带 CRC 随机数据",
                "tooltip_block_address": "输入十进制的块地址",
                "tooltip_erase_block": "擦除指定块（注意：此操作不可逆）",
                "tooltip_clear_output": "清除日志输出",
                "tooltip_data_type": "输入数据类型，格式为 0x 开头的 4 位十六进制数（如 0x5A5A）",
                "tooltip_num_blocks": "输入要测试的块数量（例如，3）",
                "tooltip_interval_custom": "输入奇数和偶数周期之间的时间间隔（单位：毫秒，例如 1000 表示 1 秒）",
                "tooltip_chip_write": "向芯片写入指定数据",
                "tooltip_chip_verify": "验证芯片数据是否正确",
                "tooltip_block_address_random": "输入十进制的块地址",
                "tooltip_cycles_random": "输入循环次数（0 表示无限循环）",
                "tooltip_lifetime_random": "执行随机数据寿命测试",
                "tooltip_pe_abl": "执行 PE ABL 测试，使用指定的块地址和循环次数",
                "tooltip_pe_eobl": "执行 PE EOBL 测试，使用指定的块地址和循环次数",
                "tooltip_block_address_custom": "输入十进制的块地址",
                "tooltip_odd_data": "输入奇数页数据，格式为 0x 开头的 4 位十六进制数（如 0x55AA）",
                "tooltip_even_data": "输入偶数页数据，格式为 0x 开头的 4 位十六进制数（如 0xAA55）",
                "tooltip_cycles_custom": "输入循环次数（0 表示无限循环）",
                "tooltip_lifetime_custom": "执行自定义数据寿命测试",
                "confirm_erase_chip_title": "确认擦除",
                "confirm_erase_chip_message": "确定要擦除整个芯片吗？此操作不可逆！",
                "confirm_erase_chip_skip_title": "确认擦除",
                "confirm_erase_chip_skip_message": "确定要擦除芯片并跳过坏块吗？此操作不可逆！",
                "confirm_erase_block_title": "确认擦除",
                "confirm_erase_block_message": "确定要擦除指定块吗？此操作不可逆！"
            }
        }

        # 当前语言（默认英文）
        self.current_language = "English"

        # 主布局
        self.central_widget = QWidget()
        self.central_widget.setStyleSheet("background-color: #F3F4F6;")
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        self.layout.setSpacing(10)
        self.layout.setContentsMargins(10, 10, 10, 10)

        # Logo 图像
        logo_label = QLabel()
        pixmap = QPixmap(resource_path("umt_logo.png"))
        scaled_pixmap = pixmap.scaled(150, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        logo_label.setPixmap(scaled_pixmap)
        logo_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(logo_label)

        # 标题标签
        header_label = QLabel("UMT FlashPro v1.0")
        header_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #111827; margin: 10px;")
        header_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(header_label)

        # 语言选择和串口选择布局
        top_layout = QHBoxLayout()
        self.language_combo = QComboBox()
        self.language_combo.addItems(["English", "Chinese"])
        self.language_combo.setFixedWidth(120)
        self.language_combo.currentTextChanged.connect(self.change_language)
        top_layout.addWidget(self.language_combo)
        top_layout.addStretch()

        self.com_combo = QComboBox()
        self.com_combo.setToolTip(self.translations[self.current_language]["tooltip_select_port"])
        top_layout.addWidget(self.com_combo)

        self.open_button = QPushButton(self.translations[self.current_language]["open_serial"])
        self.open_button.setStyleSheet("""
            background-color: #005BAC; color: white; border-radius: 5px; padding: 8px;
            QPushButton:hover { background-color: #1E88E5; }
        """)
        self.open_button.setToolTip(self.translations[self.current_language]["tooltip_open_serial"])
        top_layout.addWidget(self.open_button)
        self.layout.addLayout(top_layout)

        # 标签页
        self.tab_widget = QTabWidget()
        self.tab_widget.setStyleSheet("""
            QTabBar::tab {
                background-color: #D1D5DB; color: #111827; padding: 8px;
                border-top-left-radius: 4px; border-top-right-radius: 4px;
            }
            QTabBar::tab:selected {
                background-color: #005BAC; color: white;
            }
        """)
        self.layout.addWidget(self.tab_widget)

        # 基本功能模块
        self.basic_tab = QWidget()
        self.tab_widget.addTab(self.basic_tab, self.translations[self.current_language]["tab_basic_functions"])

        # 为 basic_tab 创建一个垂直布局，用于垂直居中
        vertical_centering_layout = QVBoxLayout(self.basic_tab)
        vertical_centering_layout.setContentsMargins(0, 0, 0, 0)

        # 在顶部添加伸缩空间以实现垂直居中
        vertical_centering_layout.addStretch()

        # 使用 QHBoxLayout 来实现水平居中
        main_layout = QHBoxLayout()  # 这里不需要指定父窗口，它会被添加到 vertical_centering_layout 中
        main_layout.setContentsMargins(0, 0, 0, 0)  # 移除外边距

        # 基本布局
        self.basic_layout = QGridLayout()
        self.basic_layout.setHorizontalSpacing(100)  # 调整水平间距为 100 像素
        self.basic_layout.setVerticalSpacing(5)  # 保持垂直间距为 5 像素

        # 左侧空白处添加容量设置（位于第 0 列）
        capacity_label = QLabel("Set Capacity")
        capacity_label.setStyleSheet("font-size: 14px; color: #111827;")
        self.basic_layout.addWidget(capacity_label, 0, 0, 1, 1)

        self.capacity_1gb_checkbox = QCheckBox("1Gb")
        self.capacity_1gb_checkbox.setStyleSheet("""
            QCheckBox { color: #111827; font-size: 12px; padding: 5px; }
            QCheckBox::indicator {
                width: 16px; height: 16px;
                border: 2px solid #6B7280;
                border-radius: 3px;
                background-color: transparent;
            }
            QCheckBox::indicator:unchecked {
                background-color: transparent;
                border: 2px solid #6B7280;
            }
            QCheckBox::indicator:checked {
                border: 2px solid #6B7280; /* 保持边框颜色一致 */
                background-color: #000000; /* 勾选时填充为黑色 */
            }
        """)
        self.capacity_1gb_checkbox.setEnabled(False)
        self.basic_layout.addWidget(self.capacity_1gb_checkbox, 1, 0)

        self.capacity_2gb_checkbox = QCheckBox("2Gb")
        self.capacity_2gb_checkbox.setStyleSheet("""
            QCheckBox { color: #111827; font-size: 12px; padding: 5px; }
            QCheckBox::indicator {
                width: 16px; height: 16px;
                border: 2px solid #6B7280;
                border-radius: 3px;
                background-color: transparent;
            }
            QCheckBox::indicator:unchecked {
                background-color: transparent;
                border: 2px solid #6B7280;
            }
            QCheckBox::indicator:checked {
                border: 2px solid #6B7280; /* 保持边框颜色一致 */
                background-color: #000000; /* 勾选时填充为黑色 */
            }
        """)
        self.capacity_2gb_checkbox.setEnabled(False)
        self.capacity_2gb_checkbox.setChecked(True)  # 默认选中 2Gb
        self.basic_layout.addWidget(self.capacity_2gb_checkbox, 2, 0)

        # 基本功能按钮（位于第 1 和第 2 列）
        self.read_id_button = QPushButton("read_ID")
        self.read_id_button.setStyleSheet("""
            background-color: #005BAC; color: white; border-radius: 5px; padding: 10px;
            QPushButton:hover { background-color: #1E88E5; }
        """)
        self.read_id_button.setFixedSize(110, 40)
        self.read_id_button.setToolTip(self.translations[self.current_language]["tooltip_read_id"])
        self.read_id_button.setEnabled(False)
        self.basic_layout.addWidget(self.read_id_button, 0, 1)

        self.badblock_button = QPushButton("bad_block")
        self.badblock_button.setStyleSheet("""
            background-color: #005BAC; color: white; border-radius: 5px; padding: 10px;
            QPushButton:hover { background-color: #1E88E5; }
        """)
        self.badblock_button.setFixedSize(110, 40)
        self.badblock_button.setToolTip(self.translations[self.current_language]["tooltip_bad_block"])
        self.badblock_button.setEnabled(False)
        self.basic_layout.addWidget(self.badblock_button, 0, 2)

        self.erase_chip_button = QPushButton("erase_chip_skip")
        self.erase_chip_button.setStyleSheet("""
            background-color: #F87171; color: white; border-radius: 5px; padding: 10px;
            QPushButton:hover { background-color: #FF9999; }
        """)
        self.erase_chip_button.setFixedSize(110, 40)
        self.erase_chip_button.setToolTip(self.translations[self.current_language]["tooltip_erase_chip"])
        self.erase_chip_button.setEnabled(False)
        self.basic_layout.addWidget(self.erase_chip_button, 1, 1)

        self.scanchipecc_button = QPushButton("scan_chip_ecc")
        self.scanchipecc_button.setStyleSheet("""
            background-color: #005BAC; color: white; border-radius: 5px; padding: 10px;
            QPushButton:hover { background-color: #1E88E5; }
        """)
        self.scanchipecc_button.setFixedSize(110, 40)
        self.scanchipecc_button.setToolTip(self.translations[self.current_language]["tooltip_scan_chip_ecc"])
        self.scanchipecc_button.setEnabled(False)
        self.basic_layout.addWidget(self.scanchipecc_button, 1, 2)

        self.erase_chip_skip_button = QPushButton("erase_chip_all")
        self.erase_chip_skip_button.setStyleSheet("""
            background-color: #F87171; color: white; border-radius: 5px; padding: 10px;
            QPushButton:hover { background-color: #FF9999; }
        """)
        self.erase_chip_skip_button.setFixedSize(110, 40)
        self.erase_chip_skip_button.setToolTip(self.translations[self.current_language]["tooltip_erase_chip_skip"])
        self.erase_chip_skip_button.setEnabled(False)
        self.basic_layout.addWidget(self.erase_chip_skip_button, 2, 1)

        self.noptest_button = QPushButton("noptest")
        self.noptest_button.setStyleSheet("""
            background-color: #005BAC; color: white; border-radius: 5px; padding: 10px;
            QPushButton:hover { background-color: #1E88E5; }
        """)
        self.noptest_button.setFixedSize(110, 40)
        self.noptest_button.setToolTip(self.translations[self.current_language]["tooltip_noptest"])
        self.noptest_button.setEnabled(False)
        self.basic_layout.addWidget(self.noptest_button, 2, 2)

        self.setwp_high_button = QPushButton("setwp_high")
        self.setwp_high_button.setStyleSheet("""
            background-color: #005BAC; color: white; border-radius: 5px; padding: 10px;
            QPushButton:hover { background-color: #1E88E5; }
        """)
        self.setwp_high_button.setFixedSize(110, 40)
        self.setwp_high_button.setToolTip(self.translations[self.current_language]["tooltip_setwp_high"])
        self.setwp_high_button.setEnabled(False)
        self.basic_layout.addWidget(self.setwp_high_button, 3, 1)

        self.setwp_low_button = QPushButton("setwp_low")
        self.setwp_low_button.setStyleSheet("""
            background-color: #005BAC; color: white; border-radius: 5px; padding: 10px;
            QPushButton:hover { background-color: #1E88E5; }
        """)
        self.setwp_low_button.setFixedSize(110, 40)
        self.setwp_low_button.setToolTip(self.translations[self.current_language]["tooltip_setwp_low"])
        self.setwp_low_button.setEnabled(False)
        self.basic_layout.addWidget(self.setwp_low_button, 3, 2)

        self.sethold_high_button = QPushButton("sethold_high")
        self.sethold_high_button.setStyleSheet("""
            background-color: #005BAC; color: white; border-radius: 5px; padding: 10px;
            QPushButton:hover { background-color: #1E88E5; }
        """)
        self.sethold_high_button.setFixedSize(110, 40)
        self.sethold_high_button.setToolTip(self.translations[self.current_language]["tooltip_sethold_high"])
        self.sethold_high_button.setEnabled(False)
        self.basic_layout.addWidget(self.sethold_high_button, 4, 1)

        self.sethold_low_button = QPushButton("sethold_low")
        self.sethold_low_button.setStyleSheet("""
            background-color: #005BAC; color: white; border-radius: 5px; padding: 10px;
            QPushButton:hover { background-color: #1E88E5; }
        """)
        self.sethold_low_button.setFixedSize(110, 40)
        self.sethold_low_button.setToolTip(self.translations[self.current_language]["tooltip_sethold_low"])
        self.sethold_low_button.setEnabled(False)
        self.basic_layout.addWidget(self.sethold_low_button, 4, 2)

        # 将 basic_layout 添加到 main_layout 中
        main_layout.addLayout(self.basic_layout)

        # 右侧空白填充
        main_layout.addStretch()

        # 将水平居中的 main_layout 添加到垂直布局中
        vertical_centering_layout.addLayout(main_layout)

        # 在底部添加伸缩空间以实现垂直居中
        vertical_centering_layout.addStretch()

        # 读写标签页
        self.rw_tab = QWidget()
        self.tab_widget.addTab(self.rw_tab, self.translations[self.current_language]["tab_pageread"])
        self.rw_layout = QGridLayout(self.rw_tab)
        self.rw_layout.setSpacing(4)

        self.page_address_input = QLineEdit()
        self.page_address_input.setPlaceholderText("Page address")
        self.page_address_input.setStyleSheet("padding: 5px; border: 2px solid #005BAC; border-radius: 5px;")
        self.page_address_input.setToolTip(self.translations[self.current_language]["tooltip_page_address"])
        self.rw_layout.addWidget(self.page_address_input, 0, 0)

        self.read_page_button = QPushButton("readpage")
        self.read_page_button.setStyleSheet("""
            background-color: #005BAC; color: white; border-radius: 5px; padding: 10px;
            QPushButton:hover { background-color: #1E88E5; }
        """)
        self.read_page_button.setFixedSize(110, 40)
        self.read_page_button.setToolTip(self.translations[self.current_language]["tooltip_read_page"])
        self.read_page_button.setEnabled(False)
        self.rw_layout.addWidget(self.read_page_button, 1, 0)

        self.otpread_button = QPushButton("otpread")
        self.otpread_button.setStyleSheet("""
            background-color: #005BAC; color: white; border-radius: 5px; padding: 10px;
            QPushButton:hover { background-color: #1E88E5; }
        """)
        self.otpread_button.setFixedSize(110, 40)
        self.otpread_button.setToolTip(self.translations[self.current_language]["tooltip_otp_read"])
        self.otpread_button.setEnabled(False)
        self.rw_layout.addWidget(self.otpread_button, 1, 1)

        # 页面范围操作标签页（page test）
        self.page_range_tab = QWidget()
        self.tab_widget.addTab(self.page_range_tab, self.translations[self.current_language]["tab_page_range_ops"])
        self.page_range_layout = QGridLayout(self.page_range_tab)
        self.page_range_layout.setSpacing(10)

        # 子区域 1：写/验证页面范围（带数据）
        write_verify_widget = QWidget()
        write_verify_layout = QGridLayout(write_verify_widget)
        write_verify_layout.setSpacing(4)

        self.start_page_input_write = QLineEdit()
        self.start_page_input_write.setPlaceholderText("Start Page")
        self.start_page_input_write.setStyleSheet("padding: 5px; border: 2px solid #005BAC; border-radius: 5px;")
        self.start_page_input_write.setToolTip(self.translations[self.current_language]["tooltip_start_page"])
        write_verify_layout.addWidget(self.start_page_input_write, 0, 0)

        self.end_page_input_write = QLineEdit()
        self.end_page_input_write.setPlaceholderText("End Page (optional)")
        self.end_page_input_write.setStyleSheet("padding: 5px; border: 2px solid #005BAC; border-radius: 5px;")
        self.end_page_input_write.setToolTip(self.translations[self.current_language]["tooltip_end_page"])
        write_verify_layout.addWidget(self.end_page_input_write, 0, 1)

        self.page_data_input = QLineEdit()
        self.page_data_input.setPlaceholderText("Enter Data (e.g., 0xFFFF)")
        self.page_data_input.setStyleSheet("padding: 5px; border: 2px solid #005BAC; border-radius: 5px;")
        self.page_data_input.setToolTip(self.translations[self.current_language]["tooltip_data_type"])
        self.page_data_input.textChanged.connect(self.validate_page_data_input)
        write_verify_layout.addWidget(self.page_data_input, 1, 0, 1, 2)  # 跨两列

        self.write_page_range_button = QPushButton("writepagerange")
        self.write_page_range_button.setStyleSheet("""
            background-color: #005BAC; color: white; border-radius: 5px; padding: 10px;
            QPushButton:hover { background-color: #1E88E5; }
        """)
        self.write_page_range_button.setFixedSize(110, 40)
        self.write_page_range_button.setToolTip(self.translations[self.current_language]["tooltip_write_page_range"])
        self.write_page_range_button.setEnabled(False)
        write_verify_layout.addWidget(self.write_page_range_button, 2, 0)

        self.verify_page_range_button = QPushButton("verifypagerange")
        self.verify_page_range_button.setStyleSheet("""
            background-color: #005BAC; color: white; border-radius: 5px; padding: 10px;
            QPushButton:hover { background-color: #1E88E5; }
        """)
        self.verify_page_range_button.setFixedSize(110, 40)
        self.verify_page_range_button.setToolTip(self.translations[self.current_language]["tooltip_verify_page_range"])
        self.verify_page_range_button.setEnabled(False)
        write_verify_layout.addWidget(self.verify_page_range_button, 2, 1)

        self.page_range_layout.addWidget(write_verify_widget, 0, 0)

        # 子区域 2：随机写/验证（无数据）
        rand_widget = QWidget()
        rand_layout = QGridLayout(rand_widget)
        rand_layout.setSpacing(4)

        self.start_page_input_rand = QLineEdit()
        self.start_page_input_rand.setPlaceholderText("Start Page")
        self.start_page_input_rand.setStyleSheet("padding: 5px; border: 2px solid #005BAC; border-radius: 5px;")
        self.start_page_input_rand.setToolTip(self.translations[self.current_language]["tooltip_start_page"])
        rand_layout.addWidget(self.start_page_input_rand, 0, 0)

        self.end_page_input_rand = QLineEdit()
        self.end_page_input_rand.setPlaceholderText("End Page")
        self.end_page_input_rand.setStyleSheet("padding: 5px; border: 2px solid #005BAC; border-radius: 5px;")
        self.end_page_input_rand.setToolTip(self.translations[self.current_language]["tooltip_end_page"])
        rand_layout.addWidget(self.end_page_input_rand, 0, 1)

        self.rand_write_crc_button = QPushButton("randwritewithcrc")
        self.rand_write_crc_button.setStyleSheet("""
            background-color: #005BAC; color: white; border-radius: 5px; padding: 10px;
            QPushButton:hover { background-color: #1E88E5; }
        """)
        self.rand_write_crc_button.setFixedSize(110, 40)
        self.rand_write_crc_button.setToolTip(self.translations[self.current_language]["tooltip_rand_write_crc"])
        self.rand_write_crc_button.setEnabled(False)
        rand_layout.addWidget(self.rand_write_crc_button, 1, 0)

        self.rand_verify_crc_button = QPushButton("randverify")
        self.rand_verify_crc_button.setStyleSheet("""
            background-color: #005BAC; color: white; border-radius: 5px; padding: 10px;
            QPushButton:hover { background-color: #1E88E5; }
        """)
        self.rand_verify_crc_button.setFixedSize(110, 40)
        self.rand_verify_crc_button.setToolTip(self.translations[self.current_language]["tooltip_rand_verify_crc"])
        self.rand_verify_crc_button.setEnabled(False)
        rand_layout.addWidget(self.rand_verify_crc_button, 1, 1)

        self.page_range_layout.addWidget(rand_widget, 1, 0)

        # 擦除模块
        self.erase_tab = QWidget()
        self.tab_widget.addTab(self.erase_tab, self.translations[self.current_language]["tab_erase"])
        self.erase_layout = QGridLayout(self.erase_tab)
        self.erase_layout.setSpacing(4)

        self.block_address_input = QLineEdit()
        self.block_address_input.setPlaceholderText("Block address")
        self.block_address_input.setStyleSheet("padding: 5px; border: 2px solid #005BAC; border-radius: 5px;")
        self.block_address_input.setToolTip(self.translations[self.current_language]["tooltip_block_address"])
        self.erase_layout.addWidget(self.block_address_input, 0, 0)

        self.erase_block_button = QPushButton("eraseblock")
        self.erase_block_button.setStyleSheet("""
            background-color: #F87171; color: white; border-radius: 5px; padding: 10px;
            QPushButton:hover { background-color: #FF9999; }
        """)
        self.erase_block_button.setFixedSize(110, 40)
        self.erase_block_button.setToolTip(self.translations[self.current_language]["tooltip_erase_block"])
        self.erase_block_button.setEnabled(False)
        self.erase_layout.addWidget(self.erase_block_button, 1, 0)

        # 添加 scanblockecc 按钮
        self.scan_block_ecc_button = QPushButton("scanblockecc")
        self.scan_block_ecc_button.setStyleSheet("""
            background-color: #005BAC; color: white; border-radius: 5px; padding: 10px;
            QPushButton:hover { background-color: #1E88E5; }
        """)
        self.scan_block_ecc_button.setFixedSize(110, 40)
        self.scan_block_ecc_button.setToolTip(self.translations[self.current_language]["tooltip_scan_block_ecc"])
        self.scan_block_ecc_button.setEnabled(False)
        self.erase_layout.addWidget(self.scan_block_ecc_button, 1, 1)

        # 输出文本框（与 Clear 和 Save 按钮水平布局）
        output_layout = QHBoxLayout()
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.output_text.setStyleSheet("background-color: #F3F4F6; color: #111827; border: 1px solid #D1D5DB;")
        # 修改字体为更美观的等宽字体
        font = QFont("Consolas", 11)  # 使用 Consolas，现代等宽字体
        font.setStyleHint(QFont.Monospace)  # 确保渲染为等宽
        self.output_text.setFont(font)
        self.output_text.setMinimumHeight(400)
        output_layout.addWidget(self.output_text)

        self.clear_button = QPushButton(self.translations[self.current_language]["clear"])
        self.clear_button.setStyleSheet("""
            background-color: #6B7280; color: white; border-radius: 5px; padding: 10px;
            QPushButton:hover { background-color: #9CA3AF; }
        """)
        self.clear_button.setFixedSize(110, 40)
        self.clear_button.setToolTip(self.translations[self.current_language]["tooltip_clear_output"])
        self.clear_button.clicked.connect(self.clear_output)
        output_layout.addWidget(self.clear_button)

        self.save_button = QPushButton(self.translations[self.current_language]["save_log"])
        self.save_button.setStyleSheet("""
            background-color: #6B7280; color: white; border-radius: 5px; padding: 10px;
            QPushButton:hover { background-color: #9CA3AF; }
        """)
        self.save_button.setFixedSize(110, 40)
        self.save_button.setToolTip(self.translations[self.current_language]["tooltip_save_log"])
        self.save_button.clicked.connect(self.save_log)
        output_layout.addWidget(self.save_button)

        self.layout.addLayout(output_layout)

        # 芯片测试模块
        self.chip_tab = QWidget()
        self.tab_widget.addTab(self.chip_tab, self.translations[self.current_language]["tab_burnin_test"])
        self.chip_layout = QGridLayout(self.chip_tab)
        self.chip_layout.setSpacing(4)

        # 数据类型输入和相关按钮
        self.data_input = QLineEdit()
        self.data_input.setPlaceholderText("Enter Data Type (e.g., 0x5A5A)")
        self.data_input.setStyleSheet("padding: 5px; border: 2px solid #005BAC; border-radius: 5px;")
        self.data_input.setToolTip(self.translations[self.current_language]["tooltip_data_type"])
        self.data_input.textChanged.connect(self.validate_data_input)
        self.chip_layout.addWidget(self.data_input, 0, 0, 1, 2)  # 跨两列

        self.chipwrite_button = QPushButton("Chip Write")
        self.chipwrite_button.setStyleSheet("""
            background-color: #005BAC; color: white; border-radius: 5px; padding: 10px;
            QPushButton:hover { background-color: #1E88E5; }
        """)
        self.chipwrite_button.setFixedSize(110, 40)
        self.chipwrite_button.setToolTip(self.translations[self.current_language]["tooltip_chip_write"])
        self.chipwrite_button.setEnabled(False)
        self.chip_layout.addWidget(self.chipwrite_button, 1, 0)

        self.chipverify_button = QPushButton("Chip Verify")
        self.chipverify_button.setStyleSheet("""
            background-color: #005BAC; color: white; border-radius: 5px; padding: 10px;
            QPushButton:hover { background-color: #1E88E5; }
        """)
        self.chipverify_button.setFixedSize(110, 40)
        self.chipverify_button.setToolTip(self.translations[self.current_language]["tooltip_chip_verify"])
        self.chipverify_button.setEnabled(False)
        self.chip_layout.addWidget(self.chipverify_button, 1, 1)

        # 时间输入和 Full Chip Random 按钮
        self.time_input_fullchiprandom = QLineEdit()
        self.time_input_fullchiprandom.setPlaceholderText("Enter Time (hours)")
        self.time_input_fullchiprandom.setStyleSheet("padding: 5px; border: 2px solid #005BAC; border-radius: 5px;")
        self.time_input_fullchiprandom.setToolTip("Enter time in hours (e.g., 1 for 1 hour)")
        self.time_input_fullchiprandom.textChanged.connect(self.validate_time_input)  # 添加验证
        self.chip_layout.addWidget(self.time_input_fullchiprandom, 2, 0, 1, 2)  # 跨两列

        self.fullchiprandom_button = QPushButton("Full Chip Random")
        self.fullchiprandom_button.setStyleSheet("""
            background-color: #005BAC; color: white; border-radius: 5px; padding: 10px;
            QPushButton:hover { background-color: #1E88E5; }
        """)
        self.fullchiprandom_button.setFixedSize(110, 40)
        self.fullchiprandom_button.setToolTip(self.translations[self.current_language]["tooltip_fullchiprandom"])
        self.fullchiprandom_button.setEnabled(False)
        self.chip_layout.addWidget(self.fullchiprandom_button, 3, 0)

        # P/E Cycles Test 标签页
        self.lifetime_tab = QWidget()
        self.tab_widget.addTab(self.lifetime_tab, self.translations[self.current_language]["tab_pe_cycles_test"])
        self.lifetime_layout = QGridLayout(self.lifetime_tab)
        self.lifetime_layout.setSpacing(4)

        # 第一行：block_address_input_random 和 cycles_input_random
        self.block_address_input_random = QLineEdit()
        self.block_address_input_random.setPlaceholderText("Enter Block Address")
        self.block_address_input_random.setStyleSheet("padding: 5px; border: 2px solid #005BAC; border-radius: 5px;")
        self.block_address_input_random.setToolTip(
            self.translations[self.current_language]["tooltip_block_address_random"])
        self.lifetime_layout.addWidget(self.block_address_input_random, 0, 0)

        self.cycles_input_random = QLineEdit()
        self.cycles_input_random.setPlaceholderText("Enter Cycles (0 for infinite)")
        self.cycles_input_random.setStyleSheet("padding: 5px; border: 2px solid #005BAC; border-radius: 5px;")
        self.cycles_input_random.setToolTip(self.translations[self.current_language]["tooltip_cycles_random"])
        self.lifetime_layout.addWidget(self.cycles_input_random, 0, 1)

        # 第二行：按钮布局
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        self.lifetime_random_button = QPushButton("Lifetime Random")
        self.lifetime_random_button.setStyleSheet("""
            background-color: #005BAC; color: white; border-radius: 5px; padding: 10px;
            QPushButton:hover { background-color: #1E88E5; }
        """)
        self.lifetime_random_button.setFixedSize(110, 40)
        self.lifetime_random_button.setToolTip(self.translations[self.current_language]["tooltip_lifetime_random"])
        self.lifetime_random_button.setEnabled(False)

        self.pe_abl_button = QPushButton("PE ABL")
        self.pe_abl_button.setStyleSheet("""
            background-color: #005BAC; color: white; border-radius: 5px; padding: 10px;
            QPushButton:hover { background-color: #1E88E5; }
        """)
        self.pe_abl_button.setFixedSize(110, 40)
        self.pe_abl_button.setToolTip(self.translations[self.current_language]["tooltip_pe_abl"])
        self.pe_abl_button.setEnabled(False)

        self.pe_eobl_button = QPushButton("PE EOBL")
        self.pe_eobl_button.setStyleSheet("""
            background-color: #005BAC; color: white; border-radius: 5px; padding: 10px;
            QPushButton:hover { background-color: #1E88E5; }
        """)
        self.pe_eobl_button.setFixedSize(110, 40)
        self.pe_eobl_button.setToolTip(self.translations[self.current_language]["tooltip_pe_eobl"])
        self.pe_eobl_button.setEnabled(False)

        button_layout.addWidget(self.lifetime_random_button)
        button_layout.addStretch()
        button_layout.addWidget(self.pe_abl_button)
        button_layout.addStretch()
        button_layout.addWidget(self.pe_eobl_button)
        self.lifetime_layout.addLayout(button_layout, 1, 0, 1, 2)

        # 第三行：num_blocks_input 和 block_address_input_custom
        self.num_blocks_input = QLineEdit()
        self.num_blocks_input.setPlaceholderText("Enter Number of Blocks (e.g., 3)")
        self.num_blocks_input.setStyleSheet("padding: 5px; border: 2px solid #005BAC; border-radius: 5px;")
        self.num_blocks_input.setToolTip(self.translations[self.current_language]["tooltip_num_blocks"])
        self.num_blocks_input.textChanged.connect(self.validate_num_blocks_input)
        self.lifetime_layout.addWidget(self.num_blocks_input, 2, 0)

        self.block_address_input_custom = QLineEdit()
        self.block_address_input_custom.setPlaceholderText("Enter Block Addresses")
        self.block_address_input_custom.setStyleSheet("padding: 5px; border: 2px solid #005BAC; border-radius: 5px;")
        self.block_address_input_custom.setToolTip(self.translations[self.current_language][
                                                       "tooltip_block_address_custom"] + " separated by spaces (e.g., 100 200 300)")
        self.block_address_input_custom.textChanged.connect(self.validate_block_addresses_input)
        self.lifetime_layout.addWidget(self.block_address_input_custom, 2, 1)

        # 第四行：odd_data_input 和 even_data_input
        self.odd_data_input = QLineEdit()
        self.odd_data_input.setPlaceholderText("Enter Odd Data (e.g., 0x55AA)")
        self.odd_data_input.setStyleSheet("padding: 5px; border: 2px solid #005BAC; border-radius: 5px;")
        self.odd_data_input.setToolTip(self.translations[self.current_language]["tooltip_odd_data"])
        self.odd_data_input.textChanged.connect(self.validate_odd_data_input)
        self.lifetime_layout.addWidget(self.odd_data_input, 3, 0)

        self.even_data_input = QLineEdit()
        self.even_data_input.setPlaceholderText("Enter Even Data (e.g., 0xAA55)")
        self.even_data_input.setStyleSheet("padding: 5px; border: 2px solid #005BAC; border-radius: 5px;")
        self.even_data_input.setToolTip(self.translations[self.current_language]["tooltip_even_data"])
        self.even_data_input.textChanged.connect(self.validate_even_data_input)
        self.lifetime_layout.addWidget(self.even_data_input, 3, 1)

        # 第五行：cycles_input_custom 和 interval_input_custom
        self.cycles_input_custom = QLineEdit()
        self.cycles_input_custom.setPlaceholderText("Enter Cycles (0 for infinite)")
        self.cycles_input_custom.setStyleSheet("padding: 5px; border: 2px solid #005BAC; border-radius: 5px;")
        self.cycles_input_custom.setToolTip(self.translations[self.current_language]["tooltip_cycles_custom"])
        self.lifetime_layout.addWidget(self.cycles_input_custom, 4, 0)

        self.interval_input_custom = QLineEdit()
        self.interval_input_custom.setPlaceholderText("Enter Interval (ms)")
        self.interval_input_custom.setStyleSheet("padding: 5px; border: 2px solid #005BAC; border-radius: 5px;")
        self.interval_input_custom.setToolTip(self.translations[self.current_language]["tooltip_interval_custom"])
        self.lifetime_layout.addWidget(self.interval_input_custom, 4, 1)

        # 第六行：lifetimetest_button
        self.lifetimetest_button = QPushButton("Lifetime Custom")
        self.lifetimetest_button.setStyleSheet("""
            background-color: #005BAC; color: white; border-radius: 5px; padding: 10px;
            QPushButton:hover { background-color: #1E88E5; }
        """)
        self.lifetimetest_button.setFixedSize(110, 40)
        self.lifetimetest_button.setToolTip("Perform lifetime test with multiple blocks using custom data")
        self.lifetimetest_button.setEnabled(False)
        self.lifetime_layout.addWidget(self.lifetimetest_button, 5, 0)

        # 状态栏
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage(self.translations[self.current_language]["disconnected"])

    def change_language(self, language):
        """切换语言并更新所有文本"""
        self.current_language = language
        t = self.translations[language]

        # 更新串口按钮和状态栏
        self.open_button.setText(
            t["open_serial"] if self.open_button.text() in [self.translations["English"]["open_serial"],
                                                            self.translations["Chinese"]["open_serial"]] else t[
                "close_serial"])
        self.open_button.setToolTip(t["tooltip_open_serial"])
        self.com_combo.setToolTip(t["tooltip_select_port"])
        self.statusBar.showMessage(
            t["disconnected"] if self.statusBar.currentMessage() in [self.translations["English"]["disconnected"],
                                                                     self.translations["Chinese"][
                                                                         "disconnected"]] else "Connected")

        # 更新标签页
        self.tab_widget.setTabText(0, t["tab_basic_functions"])
        self.tab_widget.setTabText(1, t["tab_pageread"])
        self.tab_widget.setTabText(2, t["tab_page_range_ops"])
        self.tab_widget.setTabText(3, t["tab_erase"])
        self.tab_widget.setTabText(4, t["tab_burnin_test"])
        self.tab_widget.setTabText(5, t["tab_pe_cycles_test"])

        # 更新基本功能模块
        self.read_id_button.setToolTip(t["tooltip_read_id"])
        self.badblock_button.setToolTip(t["tooltip_bad_block"])
        self.erase_chip_button.setToolTip(t["tooltip_erase_chip"])
        self.scanchipecc_button.setToolTip(t["tooltip_scan_chip_ecc"])
        self.erase_chip_skip_button.setToolTip(t["tooltip_erase_chip_skip"])
        self.noptest_button.setToolTip(t["tooltip_noptest"])
        self.setwp_high_button.setToolTip(t["tooltip_setwp_high"])
        self.setwp_low_button.setToolTip(t["tooltip_setwp_low"])
        self.sethold_high_button.setToolTip(t["tooltip_sethold_high"])
        self.sethold_low_button.setToolTip(t["tooltip_sethold_low"])

        # 更新读写模块
        self.page_address_input.setToolTip(t["tooltip_page_address"])
        self.read_page_button.setToolTip(t["tooltip_read_page"])
        self.otpread_button.setToolTip(t["tooltip_otp_read"])

        #更新页读写模块
        self.start_page_input_write.setToolTip(t["tooltip_start_page"])
        self.end_page_input_write.setToolTip(t["tooltip_end_page"])
        self.page_data_input.setToolTip(t["tooltip_data_type"])
        self.write_page_range_button.setToolTip(t["tooltip_write_page_range"])
        self.verify_page_range_button.setToolTip(t["tooltip_verify_page_range"])

        self.start_page_input_rand.setToolTip(t["tooltip_start_page"])
        self.end_page_input_rand.setToolTip(t["tooltip_end_page"])
        self.rand_write_crc_button.setToolTip(t["tooltip_rand_write_crc"])
        self.rand_verify_crc_button.setToolTip(t["tooltip_rand_verify_crc"])

        # 更新擦除模块
        self.block_address_input.setToolTip(t["tooltip_block_address"])
        self.erase_block_button.setToolTip(t["tooltip_erase_block"])
        self.scan_block_ecc_button.setToolTip(t["tooltip_scan_block_ecc"])

        # 更新日志区域
        self.clear_button.setText(t["clear"])
        self.clear_button.setToolTip(t["tooltip_clear_output"])
        self.save_button.setText(t["save_log"])
        self.save_button.setToolTip(t["tooltip_save_log"])

        # 更新芯片测试模块
        self.data_input.setToolTip(t["tooltip_data_type"])
        self.chipwrite_button.setToolTip(t["tooltip_chip_write"])
        self.chipverify_button.setToolTip(t["tooltip_chip_verify"])
        self.time_input_fullchiprandom.setToolTip("Enter time in hours (e.g., 1 for 1 hour)")
        self.fullchiprandom_button.setToolTip(t["tooltip_fullchiprandom"])

        # 更新寿命测试模块
        self.block_address_input_random.setToolTip(t["tooltip_block_address_random"])
        self.cycles_input_random.setToolTip(t["tooltip_cycles_random"])
        self.lifetime_random_button.setToolTip(t["tooltip_lifetime_random"])
        self.pe_abl_button.setToolTip(t["tooltip_pe_abl"])
        self.pe_eobl_button.setToolTip(t["tooltip_pe_eobl"])
        self.block_address_input_custom.setToolTip(t["tooltip_block_address_custom"])
        self.odd_data_input.setToolTip(t["tooltip_odd_data"])
        self.even_data_input.setToolTip(t["tooltip_even_data"])
        self.cycles_input_custom.setToolTip(t["tooltip_cycles_custom"])
        self.interval_input_custom.setToolTip(t["tooltip_interval_custom"])
        self.lifetimetest_button.setToolTip(t["tooltip_lifetime_custom"])

    def toggle_buttons(self, enabled):
        """启用或禁用所有操作按钮"""
        self.read_id_button.setEnabled(enabled)
        self.badblock_button.setEnabled(enabled)
        self.erase_chip_button.setEnabled(enabled)
        self.scanchipecc_button.setEnabled(enabled)
        self.erase_chip_skip_button.setEnabled(enabled)
        self.noptest_button.setEnabled(enabled)
        self.setwp_high_button.setEnabled(enabled)
        self.setwp_low_button.setEnabled(enabled)
        self.sethold_high_button.setEnabled(enabled)
        self.sethold_low_button.setEnabled(enabled)
        self.read_page_button.setEnabled(enabled)
        self.otpread_button.setEnabled(enabled)
        self.erase_block_button.setEnabled(enabled)
        self.scan_block_ecc_button.setEnabled(enabled)
        self.write_page_range_button.setEnabled(enabled)
        self.verify_page_range_button.setEnabled(enabled)
        self.rand_write_crc_button.setEnabled(enabled)
        self.rand_verify_crc_button.setEnabled(enabled)
        self.chipwrite_button.setEnabled(enabled)
        self.chipverify_button.setEnabled(enabled)
        self.fullchiprandom_button.setEnabled(enabled)
        self.lifetime_random_button.setEnabled(enabled)
        self.lifetimetest_button.setEnabled(enabled)
        self.pe_abl_button.setEnabled(enabled)
        self.pe_eobl_button.setEnabled(enabled)
        self.capacity_1gb_checkbox.setEnabled(enabled)  # 启用 1Gb 复选框
        self.capacity_2gb_checkbox.setEnabled(enabled)  # 启用 2Gb 复选框

    def validate_page_data_input(self, text):
        """验证 Page Range Ops 数据输入"""
        # 如果输入为空，恢复默认蓝色边框
        if not text.strip():
            self.page_data_input.setStyleSheet("padding: 5px; border: 2px solid #005BAC; border-radius: 5px;")
        # 验证输入格式
        elif not text.startswith("0x") or len(text) != 6:
            self.page_data_input.setStyleSheet("padding: 5px; border: 2px solid #EF4444; border-radius: 5px;")
        else:
            self.page_data_input.setStyleSheet("padding: 5px; border: 2px solid #10B981; border-radius: 5px;")

    def validate_data_input(self, text):
        """验证 Chip Test 数据输入"""
        # 如果输入为空，恢复默认蓝色边框
        if not text.strip():
            self.data_input.setStyleSheet("padding: 5px; border: 2px solid #005BAC; border-radius: 5px;")
        # 验证输入格式
        elif not text.startswith("0x") or len(text) != 6:
            self.data_input.setStyleSheet("padding: 5px; border: 2px solid #EF4444; border-radius: 5px;")
        else:
            self.data_input.setStyleSheet("padding: 5px; border: 2px solid #10B981; border-radius: 5px;")

    def validate_num_blocks_input(self, text):
        """验证块地址总数输入，必须为正整数"""
        if not text.strip():
            self.num_blocks_input.setStyleSheet("padding: 5px; border: 2px solid #005BAC; border-radius: 5px;")
        else:
            try:
                value = int(text)
                if value <= 0:
                    self.num_blocks_input.setStyleSheet("padding: 5px; border: 2px solid #EF4444; border-radius: 5px;")
                else:
                    self.num_blocks_input.setStyleSheet("padding: 5px; border: 2px solid #10B981; border-radius: 5px;")
            except ValueError:
                self.num_blocks_input.setStyleSheet("padding: 5px; border: 2px solid #EF4444; border-radius: 5px;")

    def validate_block_addresses_input(self, text):
        """验证块地址输入，支持多个以空格分隔的十进制地址，并与 num_blocks 匹配"""
        if not text.strip():
            self.block_address_input_custom.setStyleSheet(
                "padding: 5px; border: 2px solid #005BAC; border-radius: 5px;")
        else:
            num_blocks_text = self.num_blocks_input.text().strip()
            if not num_blocks_text:
                self.block_address_input_custom.setStyleSheet(
                    "padding: 5px; border: 2px solid #EF4444; border-radius: 5px;")
                self.append_text("Please enter the number of blocks first")
                return
            try:
                num_blocks = int(num_blocks_text)
                if num_blocks <= 0:
                    self.block_address_input_custom.setStyleSheet(
                        "padding: 5px; border: 2px solid #EF4444; border-radius: 5px;")
                    return
                addresses = text.split()
                if len(addresses) != num_blocks:
                    self.block_address_input_custom.setStyleSheet(
                        "padding: 5px; border: 2px solid #EF4444; border-radius: 5px;")
                    self.append_text("Number of blocks does not match input addresses")
                    return
                for addr in addresses:
                    if not addr.isdigit() or int(addr) < 0:
                        self.block_address_input_custom.setStyleSheet(
                            "padding: 5px; border: 2px solid #EF4444; border-radius: 5px;")
                        self.append_text("Invalid block address format")
                        return
                self.block_address_input_custom.setStyleSheet(
                    "padding: 5px; border: 2px solid #10B981; border-radius: 5px;")
            except ValueError:
                self.block_address_input_custom.setStyleSheet(
                    "padding: 5px; border: 2px solid #EF4444; border-radius: 5px;")
                self.append_text("Invalid number of blocks or address format")

    def validate_odd_data_input(self, text):
        """验证奇数页数据输入"""
        # 如果输入为空，恢复默认蓝色边框
        if not text.strip():
            self.odd_data_input.setStyleSheet("padding: 5px; border: 2px solid #005BAC; border-radius: 5px;")
        # 验证输入格式
        elif not text.startswith("0x") or len(text) != 6:
            self.odd_data_input.setStyleSheet("padding: 5px; border: 2px solid #EF4444; border-radius: 5px;")
        else:
            self.odd_data_input.setStyleSheet("padding: 5px; border: 2px solid #10B981; border-radius: 5px;")

    def validate_even_data_input(self, text):
        """验证偶数页数据输入"""
        # 如果输入为空，恢复默认蓝色边框
        if not text.strip():
            self.even_data_input.setStyleSheet("padding: 5px; border: 2px solid #005BAC; border-radius: 5px;")
        # 验证输入格式
        elif not text.startswith("0x") or len(text) != 6:
            self.even_data_input.setStyleSheet("padding: 5px; border: 2px solid #EF4444; border-radius: 5px;")
        else:
            self.even_data_input.setStyleSheet("padding: 5px; border: 2px solid #10B981; border-radius: 5px;")

    def validate_time_input(self, text):
        """验证 Full Chip Random 时间输入，支持小数"""
        if not text.strip():
            self.time_input_fullchiprandom.setStyleSheet("padding: 5px; border: 2px solid #005BAC; border-radius: 5px;")
        else:
            try:
                value = float(text)  # 支持小数
                if value <= 0:
                    self.time_input_fullchiprandom.setStyleSheet(
                        "padding: 5px; border: 2px solid #EF4444; border-radius: 5px;")
                else:
                    self.time_input_fullchiprandom.setStyleSheet(
                        "padding: 5px; border: 2px solid #10B981; border-radius: 5px;")
            except ValueError:
                self.time_input_fullchiprandom.setStyleSheet(
                    "padding: 5px; border: 2px solid #EF4444; border-radius: 5px;")

    def append_text(self, text):
        """显示日志，错误信息以红色高亮，添加时间戳"""
        # 生成时间戳，格式为 [YYYY-MM-DD HH:MM:SS]
        timestamp = datetime.datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
        # 拼接时间戳和日志内容
        log_entry = f"{timestamp} {text}"
        # 设置颜色：错误信息为红色，其他为默认颜色
        if "错误" in text or "Error" in text:
            self.output_text.setTextColor(QColor("#EF4444"))
        else:
            self.output_text.setTextColor(QColor("#111827"))
        self.output_text.append(log_entry)

    def set_open_button_text(self, text):
        if text == self.translations["Chinese"]["open_serial"]:
            self.open_button.setText(self.translations[self.current_language]["open_serial"])
        else:
            self.open_button.setText(self.translations[self.current_language]["close_serial"])

    def clear_output(self):
        self.output_text.clear()

    def save_log(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Log", "", "Text Files (*.txt);;All Files (*)")
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(self.output_text.toPlainText())
                self.append_text("Log saved successfully" if self.current_language == "English" else "日志保存成功")
            except Exception as e:
                self.append_text(
                    f"Failed to save log: {e}" if self.current_language == "English" else f"日志保存失败: {e}")

    def confirm_erase_chip(self, command_handler):
        """确认擦除芯片操作"""
        reply = QMessageBox.question(self, self.translations[self.current_language]["confirm_erase_chip_title"],
                                     self.translations[self.current_language]["confirm_erase_chip_message"],
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            command_handler.erase_chip()

    def confirm_erase_chip_skip(self, command_handler):
        """确认擦除芯片并跳过坏块操作"""
        reply = QMessageBox.question(self, self.translations[self.current_language]["confirm_erase_chip_skip_title"],
                                     self.translations[self.current_language]["confirm_erase_chip_skip_message"],
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            command_handler.erase_chip_skip()

    def confirm_erase_block(self, command_handler):
        """确认擦除块操作"""
        reply = QMessageBox.question(self, self.translations[self.current_language]["confirm_erase_block_title"],
                                     self.translations[self.current_language]["confirm_erase_block_message"],
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            command_handler.eraseblock(self.block_address_input.text())

    def update_com_ports(self, ports):
        self.com_combo.clear()
        for port in ports:
            self.com_combo.addItem(port.device)



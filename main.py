import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFont
from gui import MainWindow
from serial_comm import SerialComm
from commands import CommandHandler
from timer_dialog import TimerDialog

class MainApp:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.app.setFont(QFont("Microsoft YaHei", 10))  # 设置中文字体

        self.serial_comm = SerialComm()
        self.window = MainWindow()
        self.command_handler = CommandHandler(self.serial_comm, self.window.append_text)

        # 初始化当前容量，默认为 2048 (2Gb)
        self.current_capacity = 2048

        # 设置默认勾选状态
        self.window.capacity_2gb_checkbox.setChecked(True)
        self.window.capacity_1gb_checkbox.setChecked(False)

        # 添加容量复选框的信号连接
        self.window.capacity_1gb_checkbox.clicked.connect(self.handle_capacity_1gb)
        self.window.capacity_2gb_checkbox.clicked.connect(self.handle_capacity_2gb)

        # 连接信号和槽
        self.window.open_button.clicked.connect(lambda: self.toggle_serial())
        self.window.read_id_button.clicked.connect(self.command_handler.read_flash_id)
        self.window.badblock_button.clicked.connect(self.command_handler.badblock)
        self.window.erase_chip_button.clicked.connect(lambda: self.window.confirm_erase_chip(self.command_handler))
        self.window.scanchipecc_button.clicked.connect(self.command_handler.scanchipecc)

        self.window.setwp_high_button.clicked.connect(self.command_handler.setwp_high)
        self.window.setwp_low_button.clicked.connect(self.command_handler.setwp_low)
        self.window.sethold_high_button.clicked.connect(self.command_handler.sethold_high)
        self.window.sethold_low_button.clicked.connect(self.command_handler.sethold_low)
        self.window.erase_chip_skip_button.clicked.connect(lambda: self.window.confirm_erase_chip_skip(self.command_handler))
        self.window.noptest_button.clicked.connect(self.command_handler.noptest)

        self.window.read_page_button.clicked.connect(lambda: self.command_handler.readpage(
            self.window.page_address_input.text()
        ))
        self.window.otpread_button.clicked.connect(lambda: self.command_handler.otpread(
            self.window.page_address_input.text()
        ))

        # Page Range Ops 按钮连接
        self.window.write_page_range_button.clicked.connect(lambda: self.command_handler.writepagerange(
            self.window.start_page_input_write.text(),
            self.window.end_page_input_write.text() if self.window.end_page_input_write.text() else None,
            self.window.page_data_input.text()
        ))
        self.window.verify_page_range_button.clicked.connect(lambda: self.command_handler.verifypagerange(
            self.window.start_page_input_write.text(),
            self.window.end_page_input_write.text() if self.window.end_page_input_write.text() else None,
            self.window.page_data_input.text()
        ))
        self.window.rand_write_crc_button.clicked.connect(lambda: self.command_handler.randwritewithcrc(
            self.window.start_page_input_rand.text(),
            self.window.end_page_input_rand.text()
        ))
        self.window.rand_verify_crc_button.clicked.connect(lambda: self.command_handler.randverify(
            self.window.start_page_input_rand.text(),
            self.window.end_page_input_rand.text()
        ))

        # Erase 按钮连接
        self.window.erase_block_button.clicked.connect(lambda: self.window.confirm_erase_block(self.command_handler))
        self.window.scan_block_ecc_button.clicked.connect(lambda: self.command_handler.scanblockecc(
            self.window.block_address_input.text()
        ))

        # Chip Test 按钮连接
        self.window.chipwrite_button.clicked.connect(lambda: self.command_handler.chipwrite(
            self.window.data_input.text()
        ))
        self.window.chipverify_button.clicked.connect(lambda: self.command_handler.chipverify(
            self.window.data_input.text()
        ))
        self.window.fullchiprandom_button.clicked.connect(
            lambda: self.start_fullchiprandom(self.command_handler, self.window.time_input_fullchiprandom.text())
        )

        # Lifetime Test 按钮连接
        self.window.lifetime_random_button.clicked.connect(lambda: self.command_handler.lifetime_random(
            self.window.block_address_input_random.text(),
            self.window.cycles_input_random.text()
        ))

        self.window.pe_abl_button.clicked.connect(lambda: self.command_handler.pe_abl(
            self.window.block_address_input_random.text(),
            self.window.cycles_input_random.text()
        ))

        self.window.pe_eobl_button.clicked.connect(lambda: self.command_handler.pe_eobl(
            self.window.block_address_input_random.text(),
            self.window.cycles_input_random.text()
        ))

        self.window.lifetimetest_button.clicked.connect(self.handle_lifetimetest)

        # 默认启用复选框（即使串口未连接）
        self.window.capacity_1gb_checkbox.setEnabled(True)
        self.window.capacity_2gb_checkbox.setEnabled(True)

        # 更新串口列表
        self.window.update_com_ports(self.serial_comm.get_available_ports())

    def handle_lifetimetest(self):
        num_blocks_text = self.window.num_blocks_input.text().strip()
        block_addresses_text = self.window.block_address_input_custom.text().strip()
        odd_data = self.window.odd_data_input.text().strip()
        even_data = self.window.even_data_input.text().strip()
        cycles = self.window.cycles_input_custom.text().strip()
        interval = self.window.interval_input_custom.text().strip()

        # 修改：只要求 num_blocks_text, block_addresses_text, odd_data, even_data, cycles 必须非空
        if not num_blocks_text or not block_addresses_text or not odd_data or not even_data or not cycles:
            self.window.append_text(
                "Required fields (number of blocks, block addresses, odd data, even data, cycles) are missing")
            return

        try:
            num_blocks = int(num_blocks_text)
            if num_blocks <= 0:
                self.window.append_text("Number of blocks must be positive")
                return
            addresses = block_addresses_text.split()
            if len(addresses) != num_blocks:
                self.window.append_text("Number of blocks does not match input addresses")
                return
            block_addresses = [int(addr) for addr in addresses if addr.isdigit() and int(addr) >= 0]
            if len(block_addresses) != num_blocks:
                self.window.append_text("Invalid block address format")
                return

            # 确保 cycles 为非负整数
            cycles = int(cycles)
            if cycles < 0:
                self.window.append_text("Cycles must be non-negative")
                return

            # 修改：如果 interval 为空，则直接调用 multiblocklifetimetest，不传递 interval 参数
            if not interval:
                self.command_handler.multiblocklifetimetest(num_blocks, block_addresses, odd_data, even_data, cycles,
                                                            "")
            else:
                # 如果 interval 不为空，验证其为非负整数
                interval = int(interval)
                if interval < 0:
                    self.window.append_text("Interval must be non-negative")
                    return
                self.command_handler.multiblocklifetimetest(num_blocks, block_addresses, odd_data, even_data, cycles,
                                                            str(interval))

        except ValueError:
            self.window.append_text("Invalid input format")

    def handle_capacity_1gb(self):
        if self.window.capacity_1gb_checkbox.isChecked():
            # 取消 2Gb 的勾选
            self.window.capacity_2gb_checkbox.setChecked(False)
            # 如果当前容量不是 1024，则发送指令
            if self.current_capacity != 1024:
                self.command_handler.set_capacity(1024)
                self.current_capacity = 1024
        else:
            # 如果取消勾选 1Gb，则自动勾选 2Gb
            self.window.capacity_2gb_checkbox.setChecked(True)
            if self.current_capacity != 2048:
                self.command_handler.set_capacity(2048)
                self.current_capacity = 2048
        print(f"Current capacity set to: {self.current_capacity} blocks")  # 调试输出

    def handle_capacity_2gb(self):
        if self.window.capacity_2gb_checkbox.isChecked():
            # 取消 1Gb 的勾选
            self.window.capacity_1gb_checkbox.setChecked(False)
            # 如果当前容量不是 2048，则发送指令
            if self.current_capacity != 2048:
                self.command_handler.set_capacity(2048)
                self.current_capacity = 2048
        else:
            # 如果取消勾选 2Gb，则自动勾选 1Gb
            self.window.capacity_1gb_checkbox.setChecked(True)
            if self.current_capacity != 1024:
                self.command_handler.set_capacity(1024)
                self.current_capacity = 1024
        print(f"Current capacity set to: {self.current_capacity} blocks")  # 调试输出

    def toggle_serial(self):
        if self.serial_comm.serial_port is None or not self.serial_comm.serial_port.is_open:
            success, msg = self.serial_comm.open_serial(self.window.com_combo.currentText())
            if success:
                self.window.set_open_button_text("关闭串口")
                self.window.statusBar.showMessage("已连接")
                self.serial_comm.reader_thread.data_received.connect(self.window.append_text)
                self.serial_comm.reader_thread.start()
                self.window.append_text("串口已成功打开")
                self.window.toggle_buttons(True)
            else:
                self.window.append_text(f"打开失败: {msg}")
                self.window.toggle_buttons(False)
        else:
            msg = self.serial_comm.close_serial()
            self.window.set_open_button_text("打开串口")
            self.window.statusBar.showMessage("未连接")
            self.window.append_text("串口已关闭")
            self.window.toggle_buttons(False)

    def start_fullchiprandom(self, command_handler, time_hours):
        """处理 fullchiprandom 按钮点击，启动倒计时并执行命令"""
        try:
            time_hours = float(time_hours)  # 支持小数输入
            if time_hours <= 0:
                self.window.append_text("Error: Time must be positive")
                return
            # 立即执行命令
            command_handler.fullchiprandom(time_hours)
            # 同时启动倒计时对话框（非模态）
            timer_dialog = TimerDialog(self.window, time_hours)
            timer_dialog.show()
        except ValueError:
            self.window.append_text("Error: Invalid time value")

    def run(self):
        self.window.show()
        sys.exit(self.app.exec_())

if __name__ == '__main__':
    main_app = MainApp()
    main_app.run()
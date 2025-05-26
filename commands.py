from PyQt5.QtCore import QThread

class CommandHandler:
    def __init__(self, serial_comm, append_text_callback):
        """初始化 CommandHandler"""
        self.serial_comm = serial_comm
        self.append_text = append_text_callback

    # 基本功能指令
    def read_flash_id(self):
        self._send_command(b"read_ID\r", "Executing: Read Flash ID")

    def badblock(self):
        self._send_command(b"badblock\r", "Executing: Bad Block Scan")

    def erase_chip(self):
        self._send_command(b"erase_chip_skip\r", "Executing: Erase Chip")

    def scanchipecc(self):
        self._send_command(b"scanchipecc\r", "Executing: ECC Scan")

    def setwp_high(self):
        self._send_command(b"setwp_high\r", "Executing: Set WP High")

    def noptest(self):
        self._send_command(b"noptest\r", "Executing: NOP Test")

    def setwp_low(self):
        self._send_command(b"setwp_low\r", "Executing: Set WP Low")

    def sethold_high(self):
        self._send_command(b"sethold_high\r", "Executing: Set HOLD High")

    def sethold_low(self):
        self._send_command(b"sethold_low\r", "Executing: Set HOLD Low")

    def erase_chip_skip(self):
        self._send_command(b"erase_chip_all\r", "Executing: Erase Chip Skip Bad Blocks")


    # 新增的 Chip Test 方法
    def chipwrite(self, data_type):
        """执行 chipwrite 命令"""
        if not data_type.startswith("0x") or len(data_type) != 6:
            self.append_text(f"Invalid Data Type: {data_type}")
            return
        command = f"chipwrite {data_type}\r".encode('ascii')
        self._send_command(command, f"Executing: Chip Write with Data {data_type}")

    def chipverify(self, data_type):
        """执行 chipverify 命令"""
        if not data_type.startswith("0x") or len(data_type) != 6:
            self.append_text(f"Invalid Data Type: {data_type}")
            return
        command = f"chipverify {data_type}\r".encode('ascii')
        self._send_command(command, f"Executing: Chip Verify with Data {data_type}")

    def fullchiprandom(self, time_hours):
        """执行 fullchiprandom 命令，带时间参数"""
        try:
            time_hours = float(time_hours)
            command = f"fullchiprandom {time_hours}\r".encode('ascii')
            self._send_command(command, f"Executing: Full Chip Random for {time_hours} hours")
        except ValueError:
            self.append_text(f"Invalid time value: {time_hours}")

    # 带参数的指令
    def readpage(self, page_address):
        """执行 readpage 命令"""
        try:
            page_address = int(page_address)
            command = f"readpage {page_address}\r".encode('ascii')
            self._send_command(command, f"Executing: Read Page at Address {page_address}")
        except ValueError:
            self.append_text(f"Invalid Page Address: {page_address}")

    def otpread(self, page_address):
        """执行 otpread 命令"""
        try:
            page_address = int(page_address)
            command = f"otpread {page_address}\r".encode('ascii')
            self._send_command(command, f"Executing: OTP Read at Address {page_address}")
        except ValueError:
            self.append_text(f"Invalid Page Address: {page_address}")

    def set_capacity(self, capacity):
        """设置芯片容量，capacity 为 block 数量（如 1024 或 2048）"""
        try:
            capacity = int(capacity)
            if capacity not in [1024, 2048]:
                self.append_text(f"Error: Invalid capacity value: {capacity}. Must be 1024 or 2048.")
                return
            command = f"setcapacity {capacity}\r".encode('ascii')
            self._send_command(command,
                               f"Executing: Set Capacity to {capacity} blocks ({'1Gb' if capacity == 1024 else '2Gb'})")
        except ValueError:
            self.append_text("Error: Capacity must be a valid integer.")

    # 页面范围写入和验证指令
    def writepagerange(self, start_page, end_page=None, data="0xFFFF"):
        """执行 writepagerange 命令"""
        try:
            start_page = int(start_page)
            # 如果未提供 end_page，则与 start_page 相同
            end_page = int(end_page) if end_page is not None else start_page
            if end_page < start_page:
                self.append_text("Error: End page must be greater than or equal to start page")
                return
            # 验证 data 格式，默认为 0xFFFF
            if not data.startswith("0x") or len(data) != 6:
                self.append_text(f"Invalid Data: {data}, using default 0xFFFF")
                data = "0xFFFF"
            command = f"writepagerange {start_page} {end_page} {data}\r".encode('ascii')
            self._send_command(command, f"Executing: Write Page Range (Start: {start_page}, End: {end_page}, Data: {data})")
        except ValueError:
            self.append_text("Invalid parameters! Start page and end page must be integers.")

    def verifypagerange(self, start_page, end_page=None, data="0xFFFF"):
        """执行 verifypagerange 命令"""
        try:
            start_page = int(start_page)
            # 如果未提供 end_page，则与 start_page 相同
            end_page = int(end_page) if end_page is not None else start_page
            if end_page < start_page:
                self.append_text("Error: End page must be greater than or equal to start page")
                return
            # 验证 data 格式，默认为 0xFFFF
            if not data.startswith("0x") or len(data) != 6:
                self.append_text(f"Invalid Data: {data}, using default 0xFFFF")
                data = "0xFFFF"
            command = f"verifypagerange {start_page} {end_page} {data}\r".encode('ascii')
            self._send_command(command, f"Executing: Verify Page Range (Start: {start_page}, End: {end_page}, Data: {data})")
        except ValueError:
            self.append_text("Invalid parameters! Start page and end page must be integers.")

    def randwritewithcrc(self, start_page, end_page):
        """执行 randwritewithcrc 命令"""
        try:
            start_page = int(start_page)
            end_page = int(end_page)
            if end_page < start_page:
                self.append_text("Error: End page must be greater than or equal to start page")
                return
            command = f"randwritewithcrc {start_page} {end_page}\r".encode('ascii')
            self._send_command(command, f"Executing: Random Write with CRC (Start: {start_page}, End: {end_page})")
        except ValueError:
            self.append_text("Invalid parameters! Start page and end page must be integers.")

    def randverify(self, start_page, end_page):
        """执行 randverify 命令"""
        try:
            start_page = int(start_page)
            end_page = int(end_page)
            if end_page < start_page:
                self.append_text("Error: End page must be greater than or equal to start page")
                return
            command = f"randverify {start_page} {end_page}\r".encode('ascii')
            self._send_command(command, f"Executing: Random Verify with CRC (Start: {start_page}, End: {end_page})")
        except ValueError:
            self.append_text("Invalid parameters! Start page and end page must be integers.")

    def eraseblock(self, block_address):
        """执行 eraseblock 命令"""
        try:
            block_address = int(block_address)
            command = f"eraseblock {block_address}\r".encode('ascii')
            self._send_command(command, f"Executing: Erase Block at Address {block_address}")
        except ValueError:
            self.append_text(f"Invalid Block Address: {block_address}")

    def scanblockecc(self, block_address):
        """执行 scanblockecc 命令"""
        try:
            block_address = int(block_address)
            command = f"scanblockecc {block_address}\r".encode('ascii')
            self._send_command(command, f"Executing: Scan Block ECC at Address {block_address}")
        except ValueError:
            self.append_text(f"Invalid Block Address: {block_address}")

    def lifetime_random(self, block_address, cycles):
        """执行 lifetime_random 命令"""
        try:
            block_address = int(block_address)
            cycles = int(cycles)
            command = f"lifetime_random {block_address} {cycles}\r".encode('ascii')
            self._send_command(command, f"Executing: Lifetime Random Test (Block: {block_address}, Cycles: {cycles})")
        except ValueError:
            self.append_text("Invalid parameters! Block address and cycles must be integers.")

    def pe_abl(self, block_address, cycles):
        """执行 PE_cycles_ABL 命令"""
        try:
            block_address = int(block_address)
            cycles = int(cycles)
            command = f"PE_cycles_ABL {block_address} {cycles}\r".encode('ascii')
            self._send_command(command, f"Executing: PE ABL Test (Block: {block_address}, Cycles: {cycles})")
        except ValueError:
            self.append_text("Invalid parameters! Block address and cycles must be integers.")

    def pe_eobl(self, block_address, cycles):
        """执行 PE_cycles_EOBL 命令"""
        try:
            block_address = int(block_address)
            cycles = int(cycles)
            command = f"PE_cycles_EOBL {block_address} {cycles}\r".encode('ascii')
            self._send_command(command, f"Executing: PE EOBL Test (Block: {block_address}, Cycles: {cycles})")
        except ValueError:
            self.append_text("Invalid parameters! Block address and cycles must be integers.")

    def multiblocklifetimetest(self, num_blocks, block_addresses, odd_data, even_data, cycles, interval):
        """执行 multiblocklifetimetest 命令，支持多块地址寿命测试"""
        try:
            num_blocks = int(num_blocks)
            if num_blocks <= 0:
                self.append_text("Error: Number of blocks must be positive")
                return
            if len(block_addresses) != num_blocks:
                self.append_text("Error: Number of block addresses does not match num_blocks")
                return
            for addr in block_addresses:
                addr = int(addr)
                if addr < 0:
                    self.append_text(f"Error: Invalid block address: {addr}")
                    return
            if not odd_data.startswith("0x") or not even_data.startswith("0x"):
                self.append_text(f"Error: Invalid Data: Odd: {odd_data}, Even: {even_data}")
                return
            cycles = int(cycles)
            if cycles < 0:
                self.append_text("Error: Cycles must be non-negative")
                return
            # 如果 interval 为空或无效，则不添加延时
            block_addresses_str = " ".join(map(str, block_addresses))
            if not interval or not interval.strip():
                command = f"multiblocklifetimetest {num_blocks} {block_addresses_str} {odd_data} {even_data} {cycles}\r".encode(
                    'ascii')
                self._send_command(command,
                                   f"Executing: Multi-Block Lifetime Test (Blocks: {num_blocks} [{block_addresses_str}], Odd Data: {odd_data}, Even Data: {even_data}, Cycles: {cycles})")
            else:
                interval = int(interval)
                if interval < 0:
                    self.append_text("Error: Interval must be non-negative.")
                    return
                command = f"multiblocklifetimetest {num_blocks} {block_addresses_str} {odd_data} {even_data} {cycles} {interval}\r".encode(
                    'ascii')
                self._send_command(command,
                                   f"Executing: Multi-Block Lifetime Test (Blocks: {num_blocks} [{block_addresses_str}], Odd Data: {odd_data}, Even Data: {even_data}, Cycles: {cycles}, Interval: {interval}ms)")
        except ValueError:
            self.append_text("Error: Invalid parameters! Block addresses, cycles, and interval must be valid integers.")

    # 通用发送指令方法
    def _send_command(self, command, description):
        """发送指令到串口"""
        try:
            print(f"Command Sent: {description}")
            success, msg = self.serial_comm.send_data(command)
            if not success:
                self.append_text(f"Error: {msg}")
                print(f"Error: {msg}")
                return
            print(f"Command Data (String): {command.decode('ascii', errors='ignore')}")
            print(f"Command Data (Hex): {command.hex()}")
            self.append_text(f"{description}: Success")
        except Exception as e:
            error_message = f"Command Failed: {description}, Error: {e}"
            self.append_text(error_message)
            print(error_message)
        finally:
            QThread.msleep(500)  # 等待设备响应





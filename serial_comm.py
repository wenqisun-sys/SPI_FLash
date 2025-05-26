import serial
import serial.tools.list_ports
from PyQt5.QtCore import QThread, pyqtSignal

class SerialReaderThread(QThread):
    data_received = pyqtSignal(str)  # 信号用于将接收的数据传递给界面

    def __init__(self, serial_port):
        super().__init__()
        self.serial_port = serial_port
        self.running = True
        self.buffer = b""  # 缓冲区用于存储未处理完的数据

    def run(self):
        while self.running and self.serial_port and self.serial_port.is_open:
            try:
                if self.serial_port.in_waiting > 0:
                    data = self.serial_port.read(self.serial_port.in_waiting)
                    print(f"接收到的原始数据（十六进制）: {data.hex()}")
                    self.buffer += data

                    while b'\n' in self.buffer:
                        line, self.buffer = self.buffer.split(b'\n', 1)
                        if line:
                            # 解码为字符串，规范化换行符
                            line_str = line.decode('ascii', errors='ignore')
                            # 将可能的 \r\n 转为 \n
                            line_str = line_str.replace('\r', '')
                            self.data_received.emit(line_str)
            except Exception as e:
                self.data_received.emit(f"读取错误: {e}")
            QThread.msleep(10)

    def stop(self):
        self.running = False
        self.wait()

class SerialComm:
    def __init__(self):
        self.serial_port = None
        self.reader_thread = None

    def get_available_ports(self):
        """获取可用的串口列表"""
        return serial.tools.list_ports.comports()

    def open_serial(self, port):
        """打开指定的串口"""
        try:
            self.serial_port = serial.Serial(port, 115200, timeout=1)
            self.reader_thread = SerialReaderThread(self.serial_port)
            return True, "串口已打开"
        except Exception as e:
            return False, f"打开串口失败: {e}"

    def close_serial(self):
        """关闭当前打开的串口"""
        if self.reader_thread:
            self.reader_thread.stop()
            self.reader_thread = None
        if self.serial_port:
            self.serial_port.close()
            self.serial_port = None
        return "串口已关闭"

    def send_data(self, data):
        """向串口发送数据"""
        if self.serial_port and self.serial_port.is_open:
            try:
                bytes_written = self.serial_port.write(data)
                self.serial_port.flush()
                return True, bytes_written
            except Exception as e:
                return False, f"发送错误: {e}"
        return False, "串口未打开"
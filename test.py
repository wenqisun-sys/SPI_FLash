import serial

try:
    ser = serial.Serial('COM9', 115200, timeout=1)
    print("串口已打开")
    data_to_send = b'read_id'  # 正确发送 0x01
    print(f"发送的数据（十六进制）: {data_to_send.hex()}")
    ser.write(data_to_send)
    ser.flush()
    print("已发送 0x01")
    ser.close()
except Exception as e:
    print(f"发送失败: {e}")
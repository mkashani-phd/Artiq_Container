import serial

# Open the serial port
ser = serial.Serial(
    port='/dev/ttyUSB2',  # your device
    baudrate=115200,        # match your device's baud rate
    bytesize=serial.EIGHTBITS,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    timeout=1             # seconds
)

print(f"Connected to {ser.portstr}")

try:
    while True:
        line = ser.readline()  # read until newline or timeout
        if line:
            print(line.decode(errors='replace').strip())
except KeyboardInterrupt:
    print("\nStopping...")
finally:
    ser.close()

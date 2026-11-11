import datetime
import time
from winreg import (HKEY_CURRENT_USER, KEY_QUERY_VALUE, KEY_SET_VALUE, OpenKey,
                    QueryValueEx, REG_BINARY, SetValueEx)

def disable_proxy() -> None:
    with OpenKey(
        HKEY_CURRENT_USER,
        r'Software\Microsoft\Windows\CurrentVersion\Internet Settings\Connections',
        access=KEY_QUERY_VALUE | KEY_SET_VALUE
    ) as connections:
        settings = bytearray(QueryValueEx(connections, 'DefaultConnectionSettings')[0])
        
        # Increment version number
        settings[0x4:0x8] = (int.from_bytes(settings[0x4:0x8], 'little') + 1).to_bytes(4, 'little')

        # Disable proxy settings (set to 0)
        settings[0x8:0xc] = (0x1).to_bytes(4, 'little')

        SetValueEx(connections, 'DefaultConnectionSettings', 0, REG_BINARY, bytes(settings))

if __name__ == '__main__':
    while True:
        disable_proxy()
        print(f"Disabled at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        time.sleep(1)

#  Дан список mac-адресов, некоторые элементы которого содержат ошибки - количество символов в них менее 16.
#  Задание 1: вывести в консоль список адресов с ошибками.
#  */
# '62:8e:4a:e7:2d:7f:72:a2', 'e2:02:79:a8:77:8b:bb:d0', '3e:49:75:08:a4:5f:12:d5', '7c:6a:f5:d6:49:1a:29:ff',
# '7a:e8:03:6b:79:9a:6d:29', 'a3:9b:70:de:ae:ec:56:ac', 'e2:53:20:16:a4:12:5f:5a', 'ed:7c:50:80:34:b4:ef:9c',
# '57:9d:c7:7c:ab:ad:35:ba', 'f3:0f:ff:be:32:d9:bf:bb', 'e5:87:fe:1a:d2:69:82:3d', '39:58:c9:99:14:91:88:6e',
# '60:27:4c:c2:5d:17:66:74', 'ea:39:5a:fc:94:73:40:1a', 'e5:6d:f0:7c:fc:0e:9b:c5', 'a1:fc:a4:b6:42:21',
# '04:3d:90:70:6d:c9', 'ba:5b:28:1b:87:4c', 'f1:af:c5:ee:87:77', '74:f6:55:e5:25:21', 'b8:8c:78:6a:01:f7',
# '2d:2c:8d:a2:27:d0', '1a:ae:d3:67:97:2d', '8b:4b:7d:ad:20:b3', '04:e7:48:59:cd:ed', '77:d5:4f:3b:6e:a8:99'

# Function that checks the separators between bytes and the MAC address length
def ifProperlySepareted(mac_address):
    # Variable that stores the MAC address without separators
    cleaned_address = ''.join(filter(str.isalnum, mac_address))
    # For 48-bit addresses, the appropriate indices for separators are checked
    if len(cleaned_address) == 12 and (mac_address[2::3] == ':::::' or  # OO:OO:OO:OO:OO:OO
                                       mac_address[2::3] == '-----' or   # OO-OO-OO-OO-OO-OO
                                       mac_address[4::5] == '..'):   # OOOO.OOOO.OOOO
        return True
    # For 64-bit addresses, the appropriate indices for separators are checked
    elif len(cleaned_address) == 16 and (mac_address[2::3] == ':::::::' or # OO:OO:OO:OO:OO:OO:OO:OO
                                         mac_address[4::5] == ':::'): # OOOO:OOOO:OOOO:OOOO
        return True
    else:
        return False

# Function that checks the presence of non-hexadecimal characters in the MAC address
def ifContainsOnlyHexValues(mac_address):
    # Variable that stores the MAC address without separators
    cleaned_address = ''.join(filter(str.isalnum, mac_address))
    # A set of valid hexadecimal characters
    hex_values = set('0123456789ABCDEFabcdef')
    # Returns True if the MAC address contains only hexadecimal characters
    return set(cleaned_address).issubset(hex_values)

# Initial list of MAC addresses
mac_addresses = ["00:1A:2B:3C:4D:5E", "AA-BB-CC-DD-EE-FF", "00-23:45:67:89:AB", "12:34:56:78:9A:BC",
                 "DE:AD:BE:EF:00:01", "00-1A-2B3-C-4D-5E", "AA-BB-CC-DD-EE-FF", "12-34-56-78-9A-BC",
                 "62:8e:4a:e7:2d:7f:72:a2", "e2:02:79:a8:77:8b:bb:d0", "3e49:7508:a45f:12d5",
                 "7c-6a-f5-d6-49-1a-29-ff", "7a.e8.03.6b.79.9a.6d.29", "a3:9b:70:de:ae:ec:56:ac",
                 "001A.2B3C.4D5E", "AABB.CCDD.EEFF", "1234.5678.9ABC", "001A2B3C4D5E", "AABBCCDDEEFF",
                 "123456789ABC", "00:1A:2B:3C:4D", "AA:BB:CC:DD:EE:FF:11", "12345.6789.ABCD",
                 "001A2B3C4D5E7F", "00:1G:2H:3J:4K:5L", "ZZ:ZZ:ZZ:ZZ:ZZ:ZZ", "12-34-56-78-9X-YZ",
                 "00.1A-2B:3C/4D.5E", "AABBCC.DDEEFF", "123456-789ABC", ""]

# Set that will store invalid MAC addresses
invalid_mac_addresses = set()

for address in mac_addresses:
    # If the MAC address has inappropriate separators, incorrect length, or misplaced separators,
    # add it to the set of invalid MAC addresses
    if not ifProperlySepareted(address):
        invalid_mac_addresses.add(address)
    # If the MAC address contains values other than hexadecimal characters, add it to the set of invalid MAC addresses
    elif not ifContainsOnlyHexValues(address):
        invalid_mac_addresses.add(address)

# Print the invalid MAC addresses
print(f"Invalid MAC addresses: {invalid_mac_addresses}")
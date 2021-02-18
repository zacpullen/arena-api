

def rest_device_settings(nodemap, profile='Default'):
    print('*' * 90)
    print(f'RESETTING DEVICE SETTINGS TO \'{profile}\' PROFILE')
    print('*' * 90)
    nodemap['UserSetSelector'].value = profile
    nodemap['UserSetLoad'].execute()


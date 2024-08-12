from netmiko import ConnectHandler
import csv

# Включение логирования для отладки
import logging

logging.basicConfig(filename='netmiko_debug.log', level=logging.DEBUG)
logger = logging.getLogger("netmiko")

# Открываем файлы логирования и с адресами устройств
with open('devices.txt') as f_devices, open('log.txt', 'a') as f_log:
    devices = f_devices.read().splitlines()

    # Открываем файл с командами
    with open('commands.csv', newline='') as f_commands:
        reader = csv.reader(f_commands)
        commands = [row for row in reader]

        # Проходим по каждому микротику в списке
        print(devices)
        for device in devices:
            device_info = {
                'device_type': 'mikrotik_routeros',
                'ip': device.split(',')[0].split(':')[0],
                'port': device.split(',')[0].split(':')[1],
                'username': device.split(',')[1],
                'password': device.split(',')[2],
                'session_log': 'session_log.txt'  # Логирование сессии
            }
            prk_number = device.split(',')[0].split(':')[0].split('.')[2]

            # Подключаемся к микротику
            with ConnectHandler(**device_info) as conn:
                print(f'Connected to {device_info["ip"]}')

                # Получаем текущее приглашение
                prompt = conn.find_prompt()
                print(f'Current prompt: {prompt}')

                # Проходим по каждой команде в списке и отправляем ее на устройство
                for cmd in commands:
                    command = ''.join(cmd)  # Преобразуем список в строку
                    command = command.replace('XX', prk_number)
                    print(f'Sending command: {command}')

                    try:
                        output = conn.send_command_timing(command, strip_command=False, strip_prompt=False)
                        print(output)
                        f_log.write(f'Result for command "{command}":\n{output}\n')

                    except Exception as e:
                        print(f"An error occurred: {e}")
                        f_log.write(f'Error for command "{command}": {e}\n')

                print(f'Disconnected from {device_info["ip"]}')

print('All devices processed.')

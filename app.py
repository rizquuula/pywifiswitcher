import logging
import os

from time import sleep


class ExecutionStatus:
    ERROR = 0
    SUCCESS = 1


class SSIDConfig:
    def __init__(self, ssid, password):
        self.ssid = ssid
        self.password = password
        
    def __str__(self):
        # return f"SSID: {self.ssid}, Password: {self.password}"
        return f"SSID: {self.ssid}"


class WifiSwitcher:
    def __init__(self, wifi_config):
        self.config = wifi_config
        
    def get_connection(self, ssid, password):
        return f'networksetup -setairportnetwork en0 {ssid} {password}'


    def execute_shell_command(self, command):
        shell_call = os.popen(command)
        return shell_call.read()


    def check_execution_status(self, response, message):
        status = ExecutionStatus.SUCCESS
        if 'Could not find network' in response:
            msg = f'Exec: {response}'
            logging.warning(msg)
            if message: print(msg)
            status = ExecutionStatus.ERROR
        else:
            if message:
                print('Exec: Connection OK')
        return status


    def ping_test(self, host="google.com", message=False):
        status = os.system(f"ping -c 1 {host}")
        if status == 0:
            msg = f'Ping! OK: {status}'
            if message: print(msg)
            return True
        else:
            msg = f'Ping! ERR: {status}' 
            logging.warning(msg)
            if message: print(msg)
            return False


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO, 
        filename='wifi-switcher.log', 
        filemode='a', 
        format='%(asctime)s | %(name)s | %(levelname)s | %(message)s'
        )
    
    config = [
        SSIDConfig('"Lantai 2 Bu Dini"','ibudini17'), 
        SSIDConfig('"LANTAI BAWAH 2"', 'ibudini17'),
	SSIDConfig('"LANTAI BAWAH 1"', 'ibudini17'),
        ]
    
    app = WifiSwitcher(config)

    counter = 0
    ping_delay = 5
    
    while True:
        index = counter % len(config)
        if index == 0: counter = 0
        
        current_config = config[index]
        logging.info(current_config)
        
        conn = app.get_connection(current_config.ssid, current_config.password)
        response = app.execute_shell_command(conn)
        conn_status = app.check_execution_status(response, message=True)
        
        if conn_status == ExecutionStatus.SUCCESS:
            print(f"Connected to: {current_config.ssid}")
            
            trial = 0
            max_trial = 3
            while True:
                is_ping_success = app.ping_test()
                
                if not is_ping_success:
                    trial += 1
                    if trial >= max_trial:
                        break
                    
                sleep(ping_delay)
        
        counter += 1
        sleep(ping_delay)
        

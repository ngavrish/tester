__author__ = 'ngavrish'

class Logger:

    def __init__(self,log_path):
        self.log_path = log_path
        self.log_list = []
        self.global_log_list = []
        self.log_name = ''

    def log(self,message):
        print message
        self.log_list.append(message + "\r\n")

    def dump_to_filesystem(self):
        log_file = open(self.log_path,'w+')
        log_file.writelines(self.log_list)
        log_file.close()
        self.global_log_list = self.log_list
#        clear log
        self.log_list = []

    def get_logs(self):
        return self.global_log_list
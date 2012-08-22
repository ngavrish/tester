__author__ = 'user'

class Logger:

    __log_list = []

    def __init__(self,log_path):
        self.log_path = log_path

    def log(self,message):
        self.__log_list.append(message + "\r\n")

    def dump_to_filesystem(self):
        log_file = open(self.log_path,'w+')
        log_file.writelines(self.get_log_list())
        log_file.close()

    def get_log_list(self):
        return self.__log_list
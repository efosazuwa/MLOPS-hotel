import traceback
import sys

class CustomException(Exception):

    def __init__(self, error_message:str, error_detail:Exception):
        super().__init__(error_message)
        self.error_message = self.get_detailed_error_message(error_message, error_detail)

    @staticmethod
    def get_detailed_error_message(error_message, error_detail:Exception):
        _, _, exc_tb = sys.exc_info()

        if exc_tb:
            file_name = exc_tb.tb_frame.f_code.co_filename
            line_number = exc_tb.tb_lineno
            return f"Error occurred in {file_name}, line {line_number}: {error_message}"
        else:
            return f"Error occurred: {error_message} ({str(error_detail)})"
    
    def __str__(self):
        return self.error_message
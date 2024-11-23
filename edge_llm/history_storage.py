import os
FILE_ERROR_PATH = os.path.dirname(os.path.abspath(__file__)) + "/mistakes_history.pkl"
FILE_CONVERSION_PATH = os.path.dirname(os.path.abspath(__file__)) + "/conversion_history.pkl"
import pickle

def store_data_to_file(data, file_path):
    with open(file_path, 'wb') as file:
        pickle.dump(data, file)

def retrieve_dict_from_file(file_path):
    try:
        with open(file_path, 'rb') as file:
            data = pickle.load(file)
            print(data)
        return data
    except FileNotFoundError:
        print("File not found")
        return None
    
class HistoryStorage:
    def __init__(self):
        self.mistakes_history = retrieve_dict_from_file(FILE_ERROR_PATH) or []
        self.convert_history = retrieve_dict_from_file(FILE_CONVERSION_PATH) or []

    def store_mistake(self, mistake):
        self.mistakes_history.append(mistake)
        store_data_to_file(self.mistakes_history, FILE_ERROR_PATH)

    def store_conversion(self, conversion):
        if 'message' in conversion:
            conversion = conversion['message']
        self.convert_history.append(conversion)
        store_data_to_file(self.convert_history, FILE_CONVERSION_PATH)

    def get_mistakes(self):
        return self.mistakes_history

    def get_conversions(self):
        return self.convert_history

history = HistoryStorage()
print(history.get_mistakes())
print(history.get_conversions())
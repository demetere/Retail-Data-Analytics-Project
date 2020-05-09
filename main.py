from models.classification.classificatoin_model import classification_model
from models.regression.arima_model.arima_model import arima_model
from models.regression.prophet_model.prophet_model import prophet_model

"""
    There is requirement.txt file where is located libraries that are needed
    to run this project. 
    
    This is the file which starts the project, but before you start the project
    you need to prepare data, so to do this go to database.py, 
    configure database, which will automatically add data 
"""
def main():
    relative_path_of_config = 'database/database.ini'

    classification_model(relative_path_of_config)
    prophet_model(relative_path_of_config)
    arima_model(relative_path_of_config)

if __name__ == '__main__':
    main()

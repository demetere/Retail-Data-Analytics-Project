from models.classificatoin_model import classification_model
from models.regression.arima_model import arima_model
from models.regression.prophet_model import prophet_func

"""
    There is requirement.txt file where is located libraries that are needed
    to run this project. 
    
    This is the file which starts the project, but before you start the project
    you need to prepare data, so to do this go to database.py, 
    configure database, which will automatically add data 
"""
def main():

    classification_model()
    prophet_func()
    arima_model()



if __name__ == '__main__':
    main()

from models.champagnee import champ
from models.classificatoin_model import classification_model
from models.new_regression_model import regression
from models.regression_model import regression_model
from models.regression_model_v2 import regression_v2, main_regression

"""
    This is the file which starts the project, but before you start the project
    you need to prepare data, so to do this go to database.py and 
    configure database    
"""
def main():
    # some practice with data

    classification_model()
    #regression_model()
    #regression()
    #main_regression()



if __name__ == '__main__':
    main()

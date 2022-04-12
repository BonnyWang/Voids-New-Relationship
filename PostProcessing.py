from scipy.stats import chisquare
import pandas as pd;

# Chi value test

def getChiValue():
    print(chisquare(producedValue, trueValue));
    
if __name__ == "__main__":
    getChiValue();
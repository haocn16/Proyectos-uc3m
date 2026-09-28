# Import required dependencies
import numpy as np

def MAE(y_true: np.ndarray, y_pred: np.ndarray) -> np.float64:
    """ Implementation of the Mean Absolute Error (MAE) """

    #absolute difference between the points y_true and y_pred
    subtraction=y_true-y_pred
    error=np.abs(subtraction)

    #return the average of the errors
    return np.mean(error)


def MSE(y_true: np.ndarray, y_pred: np.ndarray) -> np.float64:
    """ Implementation of the Mean Squared Error (MSE) """
    
    #squared difference between the points
    squared=(y_true-y_pred)**2

    #return the average
    return np.mean(squared)

def R2(y_true: np.ndarray, y_pred: np.ndarray) -> np.float64:
    """ Implementation of the R2 metric """
    #consider the formula given in the statement

    #get the mean of y_true
    true_avg=np.mean(y_true)

    #get the squared errors
    squared=(y_true-y_pred)**2
    squared_errors=np.sum(squared)

    #sum of all squared y_true-true_avg
    squared_true=(y_true-true_avg)**2
    sum_squared=np.sum(squared_true)

    #if sum_squared==0, we can't divide it
    if sum_squared==0:
        return 0

    #return the answer
    answer = 1-(squared_errors/sum_squared)
    return answer

def Corr(y_true: np.ndarray, y_pred: np.ndarray) -> np.float64:
    """ Implementation of the Pearson's Correlation Coefficient """
    #calculate means
    mean_true=np.mean(y_true)
    mean_pred=np.mean(y_pred)

    #calculate covariance
    term1=y_true-mean_true
    term2=y_pred-mean_pred
    covariance=np.sum(term1*term2)

    #calculate standard deviations
    squared_true=np.sum((y_true-mean_true)**2)
    squared_pred=np.sum((y_pred-mean_pred)**2)
    standard_dev=np.sqrt(squared_true*squared_pred)

    #if standard_dev is 0, we can't divide
    if standard_dev==0:
        return 0
    
    #else, return the answer
    answer=covariance/standard_dev
    return answer


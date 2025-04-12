import numpy as np

class MultVarLinearRegressionModel:
    def __init__(self):
        self.weights = None # holds weights w1,w2,w3,wn
        self.bias = 0       # Intercept term (b)


    # This uses matrix math (called the Normal Equation) to find the best weights.
    def fit(self, X, y): 
        """
        Fit the model using the Normal Equation:
        w = (X^T X)^-1 X^T y
        """
        ones = np.ones((X.shape[0], 1))        # Column of 1s to simulate bias term
        X_b = np.hstack([ones, X])             # Augmented X with bias term
        X_transpose = X_b.T

        self.theta = np.linalg.inv(X_transpose @ X_b) @ X_transpose @ y

        self.bias = self.theta[0]              # First value = intercept
        self.weights = self.theta[1:]          # Rest = weights for each feature

    def predict(self, X):
        """
        Predict using:
        y_pred = X * w + b
        """
        return X @ self.weights + self.bias 
        # No longer loop manually, instead, this uses NumPy to predict in bulk using matrix multiplication.


    def mean_squared_error(self, y_true, y_pred):
        return np.mean((y_true - y_pred) ** 2)
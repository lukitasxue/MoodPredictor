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
    
# Learns the weights w1 to w7 and bias from the training data.
# Predict use those leared values to compute the output (mood score) from the new data 
def train_test_split(X, y, test_size=0.2, random_seed=42):
    np.random.seed(random_seed)
    indices = np.arange(X.shape[0])
    np.random.shuffle(indices)

    test_count = int(X.shape[0] * test_size)
    test_indices = indices[:test_count]
    train_indices = indices[test_count:]

    return X[train_indices], X[test_indices], y[train_indices], y[test_indices]
from sklearn.base import BaseEstimator
import numpy as np

class HuberReg(BaseEstimator):
    def __init__(self, delta=1.0, gd_type='stochastic', 
                 tolerance=1e-4, max_iter=1000, w0=None, alpha=1e-3, eta=1e-3):
        """
        gd_type: 'full' or 'stochastic'
        tolerance: for stopping gradient descent
        max_iter: maximum number of steps in gradient descent
        w0: np.array of shape (d) - init weights
        eta: learning rate
        alpha: momentum coefficient
        """
        self.delta = delta
        self.gd_type = gd_type
        self.tolerance = tolerance
        self.max_iter = max_iter
        self.w0 = w0
        self.alpha = alpha
        self.w = None
        self.eta = eta
        self.loss_history = None # list of loss function values at each training iteration
        self.h = 0
    
    def fit(self, X, y):
        """
        X: np.array of shape (l, d)
        y: np.array of shape (l)
        ---
        output: self
        """
        l = X.shape[0]
        d = X.shape[1]
        
        
        self.loss_history = np.array([])
        for epoch in range(self.max_iter):            
            if self.gd_type == 'stochastic':
                sample = np.random.randint((X.shape[0]-1))
                grad = self.calc_gradient(X[:sample], y[:sample])
            else:
                grad = self.calc_gradient(X, y)
            
            cost = self.calc_loss(X, y)
            self.loss_history = np.append(self.loss_history, cost) 
            
            if self.w is None:
                if self.alpha == 0:
                    w = self.w0 - (self.eta * grad)
                else:
                    h = self.alpha*self.h + (self.eta*grad)
                    self.h = h
                    w = self.w0 - self.h
                    
                if np.linalg.norm(w - self.w0) < self.tolerance:
                    self.w = w
                    break
                else:
                    self.w = w          


            else:
                if self.alpha == 0:
                    w = self.w - (self.eta * grad)
                else:
                    h = self.alpha*self.h + (self.eta*grad)
                    self.h = h
                    w = self.w - self.h
            
                if np.linalg.norm(w - self.w) < self.tolerance:
                    self.w = w
                    break
                else:
                    self.w = w          

                       
        
        return self
    
    def predict(self, X):
        if self.w is None:
            raise Exception('Not trained yet')
        else:
            
            return np.dot(X, self.w)
        
        
    def calc_gradient(self, X, y):
        l = X.shape[0]
        d = X.shape[1]
        
        
        X = np.array(X)
        y = np.array(y)
                
        if self.w is None:
            a = (np.dot(X,self.w0) - y).reshape((-1, 1))
        else:
            a = (np.dot(X,self.w) - y).reshape((-1, 1))
            
        gradient = np.zeros(d)
            
        bigger = np.where(np.abs(a) <= self.delta)
        least = np.where(np.abs(a) > self.delta)
        
       
        gradient = 0       
        if bigger[0].shape[0]:
            gradient = np.sum((a[bigger].reshape((-1, 1)) * X[bigger[0], :]), axis=0)
            
        if least[0].shape[0]:
            gradient += np.sum((np.sign(a[least].reshape((-1, 1))) * X[least[0], :] * self.delta), axis=0)
        
        
        return gradient / len(gradient)
        
    
        

    def calc_loss(self, X, y):
        """
        X: np.array of shape (l, d)
        y: np.array of shape (l)
        ---
        output: float 
        """ 
        
        def vec_func(difference, y, a):
            return np.vectorize(loss_for_el)(difference, y, a)

        def loss_for_el(difference, y, a):
            if difference <= self.delta:
                return ((y-a)**2)/2
            else:
                return self.delta*np.abs(y-a) - (self.delta**2)/2
            
        l = X.shape[0]
        d = X.shape[1]
        
        if self.w is None:
            a = np.dot(X, self.w0)
        else:
            a = np.dot(X, self.w)
            
        difference = np.abs(y-a)
        loss = vec_func(difference, y, a)

        return np.sum(loss)/l
        

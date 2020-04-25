import random
import math

class GausRNG:    
    """
        Box–Muller method
        
    """    
    
    def __init__(self):        
        self.ready=False
        self.second=0


    def next(self, m :float =0, d:float =1):        
        """Box–Muller method
        
        saves second value

        Keyword Arguments:
            m {float} -- mean (default: {0})
            d {float} -- standard deviation (default: {1})
        
        Returns:
            float -- random value with normal distribution N(m,d)
        """   
        if self.ready==True:
            self.ready=False
            return self.second*d+m
        else:
            while True:
                u = random.random()*2-1
                v = random.random()*2-1
                s = u**2+v**2
                if not 0<s<=1:
                    continue
                r = math.sqrt(-2*math.log(s)/s)
                self.second= r*u
                self.ready = True
                return r*v*d+m
    
    @staticmethod
    def expected_pdf(x :float, m: float=0, s :float=1):        
        """
            Probability density function of gaus distribution,
            
            static method
            
        Arguments:
            x {float} -- at

        Keyword Arguments:
            m {float} -- mean value (default: {0})
            s {float} -- standard deviation (default: {1})

        Returns:
            float -- [0,1] value
        """        
        return 1/(s*math.sqrt(2*math.pi))*math.exp(-((x-m)**2)/(2*s**2))
            
class ExpRNG:
    @staticmethod
    def next(a :float=1):
        """
            Exponential distribution
            
            static method            
            
        Keyword Arguments:
            a {float} -- mean (default: {1})

        Returns:
            float>0 -- generated random value
        """        
        return -a*math.log(random.random())
    
    @staticmethod    
    def expected_pdf(x :float,a :float=1):
        """
            Expected exponential PDF,
            
            static method

        Arguments:
            x {float} -- at

        Keyword Arguments:
            a {float} -- mean (default: {1})

        Returns:
            float -- [0,1] value, 0 if x<0
        """        
        return (1/a)*math.exp(-x/a) if x>=0 else 0
            
if __name__ == "__main__":
    rng = GausRNG()
    a = rng.next()
    print(a)
    
    rng_exp = ExpRNG()    
    b =ExpRNG.next()  #rng_exp.next()    
    print(b)
import plotly.graph_objects as go
import numpy as np
import math

from Distribution import GausRNG
from Distribution import ExpRNG

class RNGTest:
    def __init__(self,
                  rng_next,
                  expected_distribution=None,
                  raw_moments :list=[1],                                   
                  central_moments :list=[2],
                  rng_calls :int=100000):
        self.rng_next=rng_next
        self.expected_distribution=expected_distribution
        self.rng_calls=rng_calls
        self.values=[]
        self.fig = go.Figure()
        for i in range(rng_calls):
            self.values.append(self.rng_next())
            
        self.raw_moments={}
        self.central_moments={}
        
        for k in raw_moments:
            self.raw_moments[k]=self.raw_moment(k)
            
        for k in central_moments:
            self.central_moments[k]=self.central_moment(k)
                   
        
            
    def raw_moment(self, k :int):
        if k in self.raw_moments:
            return self.raw_moments[k]
        return sum([x**k for x in self.values])/len(self.values)
    
    def central_moment(self, k :int):
        if k in self.central_moments:
            return self.central_moments[k]
                
        mean = self.raw_moment(1)
        v  = sum([(x-mean)**k for x in self.values])/len(self.values)
        print(v)
        self.central_moments[k] = v
        return self.central_moments[k]
        
    def Draw(self,x_from, x_to, bins):        
        self.fig.add_trace(
            go.Histogram(
                x=self.values,
                histnorm='probability density',
                name='distribution', # name used in legend and hover labels
                opacity=0.8,
                xbins=dict( # bins used for histogram
                    start=x_from,
                    end=x_to,
                    size=(x_to-x_from)/bins
                )
            )
        )
        if not self.expected_distribution is None:
            self.fig.add_trace(
                go.Scatter(
                    x = np.arange(x_from,x_to,0.2),
                    y = [self.expected_distribution(x) for x in np.arange(x_from,x_to,0.2)],
                    name = "expected distribution"
                )
            )
        self.fig.show()

if __name__ == "__main__":
    steps = 100000
    mean=0
    d = 2
    sign = math.sqrt(d)
    x_from, x_to = -10,10
    bins = 100

    
    rng = GausRNG()
    t = RNGTest(
        rng_next = lambda : rng.next(mean,sign),
        expected_distribution = lambda x: rng.expected_pdf(x,mean,sign)
        )
    t.Draw(x_from,x_to,bins)
    print("E = {m:3f}, D = {d:.3f}".format(
        m = t.raw_moment(1),
        d = t.central_moment(2)
    ))
    
    exp_mean = 3
    t = RNGTest(
        rng_next= lambda: ExpRNG.next(exp_mean),
        expected_distribution= lambda x: ExpRNG.expected_pdf(x,exp_mean)
    )
    print("E = {m:3f}, D = {d:.3f}".format(
        m = t.raw_moment(1),
        d = t.central_moment(2)
    ))
    t.Draw(-1, 10,bins)
                   
        
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import numpy as np
import math
import random
import statistics 

from Distribution import GausRNG
from Distribution import ExpRNG




class CTRW:
    """
        Continuous-time random walk
    
        point starts at (0,0), waits for random T with exponential distribution 
        and jumps for R given by N(m,s)**2 in uniformly random direction 
        
        saves points as (x: float,y: float) in self.p
        moments of jump in list self.t
        range of jump, angle and waiting time in lists self.dr, self.fi, self.dt       
        
    """    
    def __init__(self):
        self.t_rng = ExpRNG()
        self.r_rng = GausRNG()
        
        self.p = [(0,0)]
        self.t = [0]
        
        self.dr = []
        self.dt = []
        self.fi = []
        
        self.last_pos = None
        
        
    def simulate(self, T: float):
        """
            Simulates behavior until time = T

        Arguments:
            T {float} -- time to simulate
        """        
        while self.t[-1]<T:
            fi = random.random()*2*math.pi
            self.fi.append(fi)
            
            dr = random.betavariate(0.5,0.5)  #self.r_rng.next(10,1)**2
            self.dr.append(dr)
            
            dt = self.t_rng.next()
            self.dt.append(dt)
            
            self.p.append((
                    self.p[-1][0]+dr*math.cos(fi),
                    self.p[-1][1]+dr*math.sin(fi)                    
                ))
            self.t.append(self.t[-1]+dt)
    
    
    def pos_at_t(self, T, save_last_call :bool=False):
        """            
            Finds position of point in moment T if system is simulated up to this time
            or returns last position

        Arguments:
            T {float} -- moment of time

        Keyword Arguments:
            save_last_call {bool} -- if False - searchs throw all list of conditions
                                     if True  - starts from positin, found in last call 
                                        (default: {False})

        Returns:
            (float, float) -- (x, y) position
        """          
        if self.last_pos is None:
            self.last_pos = 0
        
        for i in range(self.last_pos,len(self.t)):
            if self.t[i]<=T<self.t[i+1]:
                self.last_pos = i
                return self.p[i]
        
        return self.p[-1]
            
            

if __name__ == "__main__":
    ctrw = CTRW()
    ctrw.simulate(10000)

    
    fig = make_subplots(rows=2, cols=2)

    path_fig = go.Scatter(
            x= [p[0] for p in ctrw.p], 
            y =[p[1] for p in ctrw.p]
        )
    dr_fig =go.Histogram(
            x=ctrw.dr,
            histnorm='probability density',
            name='dr distribution'
            )
    
    fi_fig = go.Histogram(
            x=ctrw.fi,
            histnorm='probability density',
            name='fi distribution',
            xbins=dict(
                size=0.1
            ))
    
    dt_fig = go.Histogram(
            x=ctrw.dt,
            histnorm='probability density',
            name='dt distribution',
            xbins=dict(
                size=0.1
            )
        )
    
    fig.add_trace(path_fig, 1, 1)
    fig.add_trace(dr_fig, 1, 2)
    fig.add_trace(fi_fig, 2, 1)
    fig.add_trace(dt_fig, 2, 2)
    
    fig.show()
    
    # Средний Квадрат
    
    group = [CTRW() for i in range(1000)]
    
    for g in group:
        g.simulate(100)
    
    x= range(100)
    y = []
    
    for t in x:
        points = [ g.pos_at_t(t,True) for g in group ]
        y.append(
            statistics.mean([p[0]**2+p[1]**2 for p in points])
            )
        
    mean_r_squared_fig=go.Figure(
      go.Scatter(
            x=[x for x in range(100)], 
            y =y
        )
    )
    
    mean_r_squared_fig.show()

            

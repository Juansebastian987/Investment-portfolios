from math import ceil,floor,isnan
from datetime import datetime
import pandas as pd
import numpy as np
from scipy.optimize import minimize
from clr import AddReference
AddReference("System")
AddReference("QuantConnect.Algorithm")
AddReference("QuantConnect.Algorithm.Framework")
AddReference("QuantConnect.Common")

from System import *
from QuantConnect import *
from QuantConnect.Orders import *
from QuantConnect.Algorithm import *
from QuantConnect.Algorithm.Framework import *
from QuantConnect.Algorithm.Framework.Alphas import *
from QuantConnect.Algorithm.Framework.Execution import *
from QuantConnect.Algorithm.Framework.Portfolio import *
from QuantConnect.Algorithm.Framework.Risk import *
from QuantConnect.Algorithm.Framework.Selection import *
from datetime import timedelta

# Creamos la clase que va a contener todo el Robo-Advisor para un perfil agresivo con un
# horizonte de inversión a medio plazo. Este algoritmo tiene el Asset Allocation clasico de markowitz  
# y el sistema all weather portfolio
class RoboAdvisorAM(QCAlgorithm):

    # Inicializamos las variables que vamos a usar en el presente algoritmo
    def Initialize(self):
        
        # Inicializamos la fecha con la cual el sistema va a hacer el analisis de los
        # datos del mercado.
        self.SetStartDate(2016, 1, 1)
        
        # Inicializamos la cantidad de dinero que va a manejar la estrategia
        # A un valor de XXXXX dolares
        # Es decir una cantidad  XXXX pesos colombianos
        self.SetCash(10000)

        # Inicializamos las variables que vamos a trabajar en este perfil y horizonte de inversión
        tickers = [
                    "VO",
                    "VUG",
                    "ACES",
                    "HTEC",
                    "GXC",
                    "FINX",
                    "CHIQ",
                    "IYK",
                    "QQQ",
                    "ESGV",
                    "SKYY",
                    "CQQQ",
                    "VTI",
                    "XSW",
                    "ARKK",
                    "ARKQ",
                    "ARKW",
                    "ARKG",
                    "ARKF",
                    ]

        # Guardamos los simbolos que se van a usar, en este caso los simbolos hacen referencia a los
        # tickers o stocks que seran los ETFs que en este perfil y horizonte se van a usar, en este
        # caso tambien lo que se hace es tomar los precios del ETF diario y guardar ese elemento
        # ademas, se guardar los ultimos 252 prices que se han hecho para luego visualizarlo.
        self.symbols = [] 
        for i in tickers:
            self.symbols.append(self.AddEquity(i, Resolution.Daily).Symbol)
        for syl in self.symbols:
            syl.window = RollingWindow[TradeBar](252) 

        # Configuramos cuales van a ser los ETF que se van a rebalancear
        for sym in self.symbols:
            self.Schedule.On(self.DateRules.MonthStart(sym), self.TimeRules.AfterMarketOpen(sym), Action(self.Rebalancing))

        # Este ETF va ser nuestro Benchmark por lo que lo guardamos como un simbolo aparte para
        # posteriormente poderlo usar
        self.spy = self.AddEquity("SPY", Resolution.Daily).Symbol

        # Establecemos el Benchmark
        # No lo configuramos para obtener solo un valor sino para que obtener todos los valores 
        # a lo largo del tiempo
        # Y añadimos los valores del Benchmark al portafolio para posteriormente hacer las comparativas
        self.SetBenchmark("SPY")
        self.lastBenchmarkValue = None
        self.BenchmarkPerformance = self.Portfolio.TotalPortfolioValue
        
        self.UniverseSettings.Resolution = Resolution.Minute

        # Configuramos los modelos del framework para el manejo del riego del portafolio
        self.SetUniverseSelection(ManualUniverseSelectionModel(tickers))
        self.SetAlpha(ConstantAlphaModel(InsightType.Price, InsightDirection.Up, timedelta(minutes = 20), 0.025, None))
        #self.SetPortfolioConstruction(EqualWeightingPortfolioConstructionModel())
        self.SetExecution(ImmediateExecutionModel())

        # Configuramos el riesgo maximo que estamos dispuestos a asumir
        riskModel = CompositeRiskManagementModel(MaximumDrawdownPercentPortfolio(0.25))
        riskModel.AddRiskManagement(MaximumUnrealizedProfitPercentPerSecurity(0.25))
        
        # Configuramos el riesgo maximo que estamos dispuestos a asumir
        self.SetRiskManagement(MaximumDrawdownPercentPortfolio(0.25))
        self.AddRiskManagement(MaximumUnrealizedProfitPercentPerSecurity(0.25))

    # Definimos los datos de nuestro algirtmo, en espcial los que son para posteriormente
    # mostrar en pantalla, es decir, todos los graficos de comparativa de nuestro algoritmo
    def OnData(self, data):
        # Guarda el precio de cierre del ETF SPY
        benchmark = self.Securities["SPY"].Close
        
        # Verifica que el ultimo valor no sea nulo y calcula el valor del Benchmark para agregarlo
        # al comparativo con el portafolio.        
        if self.lastBenchmarkValue is not  None:
           self.BenchmarkPerformance = self.BenchmarkPerformance * (benchmark/self.lastBenchmarkValue)
       
        # Guarda el precio de cierre de referencia de hoy para utilizarlo mañana
        self.lastBenchmarkValue = benchmark
        
        # Aqui configuramos nuestro algoritmo con nuestro Benchmark
        self.Plot("Strategy vs Benchmark", "Portfolio Value", self.Portfolio.TotalPortfolioValue)
        self.Plot("Strategy vs Benchmark", "Benchmark", self.BenchmarkPerformance)

    # Definimos el metodo que va a rebalancear los  
    def Rebalancing(self):
        data = {}
        for syl in self.symbols:
            data[syl] = [float(i.Close) for i in syl.window]
        df_price = pd.DataFrame(data,columns=data.keys()) 
        daily_return = (df_price / df_price.shift(1)).dropna()
            
        a = PortfolioOptimization(daily_return, 0, len(data))
        opt_weight = a.opt_portfolio()  
            
        if isnan(sum(opt_weight)): return
        self.Log(str(opt_weight))
        
        for i in range(len(data)):
            self.SetHoldings(df_price.columns[i], opt_weight[i])
            
            # En este caso pondero algunos ETFs que se considera tenga mas proyección
            # Esta estrategia es la utilizada en All Weather para tener las ponderaciones
            # dia a dia de las acciones que queremos tener siempre con un peso especifico en cartera

        
class PortfolioOptimization(object):

    import numpy as np
    import pandas as pd

    def __init__(self, df_return, risk_free_rate, num_assets):
        
        self.daily_return = df_return
        self.risk_free_rate = risk_free_rate
        self.n = num_assets # número de activos de riesgo en la cartera
        self.target_vol = 0.25

    def annual_port_return(self, weights):
        # Calcular la rentabilidad anual de la cartera
        return np.sum(self.daily_return.mean() * weights) * 252

    def annual_port_vol(self, weights):
        # Calculamos la volatilidad anual de la cartera
        return np.sqrt(np.dot(weights.T, np.dot(self.daily_return.cov() * 252, weights)))

    def min_func(self, weights):
        
        # Metodo 1: maximizar el sharp ratio
        return - self.annual_port_return(weights) / self.annual_port_vol(weights)
        
        # Metodo 2: maximizar la rentabilidad con la volatilidad objetivo 
        # return - self.annual_port_return(weights) / self.target_vol

    def opt_portfolio(self):
        # maximizar el ratio sharpe para encontrar las ponderaciones óptimas
        cons = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
        bnds = tuple((0, 1) for x in range(2)) + tuple((0, 0.25) for x in range(self.n - 2))
        opt = minimize(self.min_func,                               # función objetivo
                       np.array(self.n * [1. / self.n]),            # valor inicial
                       method='SLSQP',                              # método de optimización
                       bounds=bnds,                                 # blímites de las variables 
                       constraints=cons)                            # condiciones de restricción
                      
        opt_weights = opt['x']
 
        return opt_weights
# This code has personal modifications for the degree project "Prototype Robo-Advisor as a 
# system for the optimization and risk management of an investment portfolio" but part of the 
# following Quanconnect code is expressed below.
#
# QUANTCONNECT.COM - Democratizing Finance, Empowering Individuals.
# Lean Algorithmic Trading Engine v2.0. Copyright 2014 QuantConnect Corporation.
# 
# Licensed under the Apache License, Version 2.0 (the "License"); 
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import clr
clr.AddReference("System")
clr.AddReference("QuantConnect.Algorithm")
clr.AddReference("QuantConnect.Common")

from System import *
from QuantConnect import *
from QuantConnect.Algorithm import *

import numpy as np
from sklearn.linear_model import LinearRegression

class ScikitLearnLinearRegressionAlgorithm(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2020, 1, 1)

        self.lookback = 30 # número de días previos de training
        
        self.SetCash(100000)
        spy = self.AddEquity("SPY", Resolution.Minute)
        
        tickers = [ "IEI",
                    "VO",
                    "CQQQ",
                    "ARKK",
                    "ARKQ",
                    "DIA",
                    "XLV",
                    "GLD",
                    "IVV",
                    "NOBL",
                    "SPY"
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

        self.Schedule.On(self.DateRules.EveryDay("SPY"), self.TimeRules.AfterMarketOpen("SPY", 28), self.Regression)
        self.Schedule.On(self.DateRules.EveryDay("SPY"), self.TimeRules.AfterMarketOpen("SPY", 30), self.Trade)
        
    
    def Regression(self):
        # Los datos históricos diarios se utilizan para entrenar el modelo de aprendizaje automático
        history = self.History(self.symbols, self.lookback, Resolution.Daily)

        # diccionario de precios: clave: símbolo; valor: precio histórico
        self.prices = {}
        # diccionario de pendientes: clave: símbolo; valor: pendiente
        self.slopes = {}
        
        for symbol in self.symbols:
            if not history.empty:
                # Obtener el precio histórico de apertura
                self.prices[symbol] = list(history.loc[symbol.Value]['open'])

        # A es la matriz de diseño
        A = range(self.lookback + 1)
        
        for symbol in self.symbols:
            if symbol in self.prices:
                # respuesta
                Y = self.prices[symbol]
                # características
                X = np.column_stack([np.ones(len(A)), A])
                
                # preparación de datos
                length = min(len(X), len(Y))
                X = X[-length:]
                Y = Y[-length:]
                A = A[-length:]
                
                # ajustar la regresión lineal
                reg = LinearRegression().fit(X, Y)
                
                # ejecutar la regresión lineal y = ax + b
                b = reg.intercept_
                a = reg.coef_[1]
                
                # almacenar las pendientes de los símbolos
                self.slopes[symbol] = a/b
                
    
    def Trade(self):
        # si no hay precio abierto
        if not self.prices:
            return 
        
        thod_buy = 0.001 # umbral de pendiente para comprar
        thod_liquidate = -0.001 # umbral de pendiente para liquidar
        
        for holding in self.Portfolio.Values:
            slope = self.slopes[holding.Symbol] 
            # liquidar cuando la pendiente es menor que thod_liquidate
            if holding.Invested and slope < thod_liquidate:
                self.Liquidate(holding.Symbol)
        
        for symbol in self.symbols:
            # comprar cuando la pendiente es mayor que thod_buy
            if self.slopes[symbol] > thod_buy:
                self.SetHoldings(symbol, 1 / len(self.symbols))
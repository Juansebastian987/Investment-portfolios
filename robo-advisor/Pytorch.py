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
import torch
import torch.nn.functional as F

class PytorchNeuralNetworkAlgorithm(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2020, 1, 1)  # Set Start Date

        self.lookback = 30 # number of previous days for training
        
        self.SetCash(100000)  # Set Strategy Cash
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
            
        self.Schedule.On(self.DateRules.EveryDay("SPY"), self.TimeRules.AfterMarketOpen("SPY", 28), self.NetTrain) # train the NN
        self.Schedule.On(self.DateRules.EveryDay("SPY"), self.TimeRules.AfterMarketOpen("SPY", 30), self.Trade)
    
    def NetTrain(self):
        # Los datos históricos diarios se utilizan para entrenar el modelo de aprendizaje automático
        history = self.History(self.symbols, self.lookback + 1, Resolution.Daily)
        
        # dicts que almacenan los precios para la formación
        self.prices_x = {} 
        self.prices_y = {}
        
        # dicts que almacenan los precios de venta y compra
        self.sell_prices = {}
        self.buy_prices = {}
        
        for symbol in self.symbols:
            if not history.empty:
                # x: depredadores; y: respuesta
                self.prices_x[symbol] = list(history.loc[symbol.Value]['open'])[:-1]
                self.prices_y[symbol] = list(history.loc[symbol.Value]['open'])[1:]
                
        for symbol in self.symbols:
            # si este símbolo tiene datos históricos
            if symbol in self.prices_x:
                
                net = Net(n_feature=1, n_hidden=10, n_output=1)     # define the network
                optimizer = torch.optim.SGD(net.parameters(), lr=0.2)
                loss_func = torch.nn.MSELoss()  # this is for regression mean squared loss
                
                for t in range(200):
                    # Obtener los datos y hacer el preprocesamiento
                    x = torch.from_numpy(np.array(self.prices_x[symbol])).float()
                    y = torch.from_numpy(np.array(self.prices_y[symbol])).float()
                    
                    # Descomprimir los datos (ver el documento de pytorch para más detalles)
                    x = x.unsqueeze(1) 
                    y = y.unsqueeze(1)
                
                    prediction = net(x)     # entrada x y predicción basada en x

                    loss = loss_func(prediction, y)     # debe ser (1. nn salida, 2. objetivo)

                    optimizer.zero_grad()   # borrar gradientes para el próximo tren
                    loss.backward()         # retropropagación, calcular los gradientes
                    optimizer.step()        # aplicar gradientes
            
            # Sigue la tendencia    
            self.buy_prices[symbol] = net(y)[-1] + np.std(y.data.numpy())
            self.sell_prices[symbol] = net(y)[-1] - np.std(y.data.numpy())
        
    def Trade(self):
        ''' 
        Entrar o salir de posiciones en función de la relación del precio de apertura de la barra actual y los precios definidos por el modelo de aprendizaje automático.
        Liquida si el precio abierto está por debajo del precio de venta y compra si el precio abierto está por encima del precio de compra 
        ''' 
        for holding in self.Portfolio.Values:
            if self.CurrentSlice[holding.Symbol].Open < self.sell_prices[holding.Symbol] and holding.Invested:
                self.Liquidate(holding.Symbol)
            
            if self.CurrentSlice[holding.Symbol].Open > self.buy_prices[holding.Symbol] and not holding.Invested:
                self.SetHoldings(holding.Symbol, 1 / len(self.symbols))

            
        
# Clase para el modelo Pytorch NN
class Net(torch.nn.Module):
    def __init__(self, n_feature, n_hidden, n_output):
        super(Net, self).__init__()
        self.hidden = torch.nn.Linear(n_feature, n_hidden)   # capa oculta
        self.predict = torch.nn.Linear(n_hidden, n_output)   # capa de salida
    
    def forward(self, x):
        x = F.relu(self.hidden(x))      # función de activación para la capa oculta
        x = self.predict(x)             # salida lineal
        return x
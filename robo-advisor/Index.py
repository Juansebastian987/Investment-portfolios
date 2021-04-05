class OptimizedHorizontalComputer(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2020, 1, 1) # Año, mes, dia
        self.SetCash(1500)
        self.vug = self.AddEquity("VUG", Resolution.Daily).Symbol
        self.arkk = self.AddEquity("ARKK",Resolution.Daily).Symbol
        self.vti = self.AddEquity("VTI",Resolution.Daily).Symbol
        self.vig = self.AddEquity("VIG",Resolution.Daily).Symbol
        self.gld = self.AddEquity("GLD", Resolution.Daily).Symbol

        self.spy = self.AddEquity("SPY", Resolution.Daily).Symbol

        # Configuramos Benchmark
        self.SetBenchmark("SPY")
        self.lastBenchmarkValue = None
        self.BenchmarkPerformance = self.Portfolio.TotalPortfolioValue

    def OnData(self, data):
        # Almacenamos el precio de cierre del Benchmark
        benchmark = self.Securities["SPY"].Close
        
        # Ingreamos las cantidades de nuestro portafolio
        if not self.Portfolio.Invested:
            self.SetHoldings("VO",    0.25)
            self.SetHoldings("SPY",   0.25)
            self.SetHoldings("GLD",   0.125)
            self.SetHoldings("CQQQ",  0.0625)
            self.SetHoldings("ARKK",  0.0625)
            self.SetHoldings("ARKQ",  0.0625)
            self.SetHoldings("XLV",   0.0625)
            self.SetHoldings("IVV",   0.0625)
            self.SetHoldings("NOBL",  0.0625)

        # Calculamos el rendimiento de nuestro punto de referencia y actualizar el valor de nuestro punto de referencia para el trazado
        if self.lastBenchmarkValue is not  None:
           self.BenchmarkPerformance = self.BenchmarkPerformance * (benchmark/self.lastBenchmarkValue)
        # Almacenamos el precio de cierre de referencia de hoy para utilizarlo mañana
        self.lastBenchmarkValue = benchmark
        # hacer nuestras graficas
        self.Plot("Strategy vs Benchmark", "Portfolio Value", self.Portfolio.TotalPortfolioValue)
        self.Plot("Strategy vs Benchmark", "Benchmark", self.BenchmarkPerformance)
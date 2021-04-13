## Execute algorithms

To execute the algorithms you must use the Quanconnect platform. This platform allows the execution of the algorithm, backtesting and execution in real time with the broker of your choice and that supports the platform.

So to log in we create an account by clicking on Sign In and then at the bottom of the page in Sign Up

<img src="https://i.postimg.cc/8PB0WGdp/crear-Cuenta.png" width="1000">

Once we enter we will have the following window

<img src="https://i.postimg.cc/Vk3xzgmp/inicio.png" width="1000">

In it we click on Create New Algorithm, it is important to highlight that we are only going to test 1 portfolio in this case the portfolio with moderate profile with a short term investment horizon and it is important to highlight that for each portfolio must be created in a new algorithm (which would be executed in different nodes, later we will address this). 

Note that at the bottom should appear PY (Python) if it does not, click on the nut option and change it.

<img src="https://i.postimg.cc/YSYJ0FS9/cambio.png" width="1000">

When we create the project we will see the following characteristics, we do not select any of them, and we click Exit Builder Mode

<img src="https://i.postimg.cc/ZRmXdq9L/opciones.png" width="1000">

The following information will be displayed

<img src="https://i.postimg.cc/BnLWWk92/main.png" width="1000">

So we proceed to paste the source code that is in the git repository https://github.com/Juansebastian987/Investment-portfolios/blob/main/robo-advisor/PortafolioMC.py

<img src="https://i.postimg.cc/NFDYSynN/main-Cambiado.png" width="1000">

In the options on the right we click on the project description and we can see what this algorithm does.

<img src="https://i.postimg.cc/hvcc282z/descripci-n.png" width="1000">

And in the upper part click on Backtest, we wait for the code to load. 

<img src="https://i.postimg.cc/25LkySq6/backtesting.png" width="1000">

After a few minutes we will get the results of our algorithm.

<img src="https://i.postimg.cc/xCK9Gp3V/resultados.png" width="1000">

What we are going to do is to modify the distribution of the data, so we drag all the results below the obtained profitability graph.

<img src="https://i.postimg.cc/pL6VPFL4/resultados2.png" width="1000">

In addition, we zoom out the display and leave the Select Chart items as follows

<img src="https://i.postimg.cc/LXdH1FfV/resultado3.png" width="1000">

<img src="https://i.postimg.cc/W13bRnT0/resultado4.png" width="1000">

As we can see we can make an analysis of our algorithm and its behavior over time, but we can also make an analysis of the transactions made and a report of the same, with which all the information is condensed and arranged in a better way to make different in-depth analysis, for this we click on the Report option.

<img src="https://i.postimg.cc/4NwNFMkJ/resultados5.png" width="1000">

We click on the button to generate the report and the platform will start to do it, this takes a couple of minutes and depends on the algorithm built, so some algorithms may take longer than others.

<img src="https://i.postimg.cc/fTMRCsP2/report.png" width="1000">

Once the report is generated, we will see the following display and click on download report

<img src="https://i.postimg.cc/2jQ5ny0L/reporte-generado.png" width="1000">

A window will be displayed and will show us a PDF with the information collected by our algorithm, in it will be key information of our system with respect to the rotation, market, biggest drop that was had in the portfolio, performance, capital that could support our system, the returns of the same in each month visualized in a heat map, the accumulated returns of our algorithm (Backtest) and our Benchmark, which in this case has been the Standard & Poor's 500 index, then we will have the returns that we could have had year after year with our portfolio, the percentage of each asset among other relevant information of the same.

<img src="https://i.postimg.cc/X7wGQxxL/reporte1.png" width="1000">

<img src="https://i.postimg.cc/N00KGttC/report2.png" width="1000">

<img src="https://i.postimg.cc/rwjdLmBt/reporte3.png" width="1000">

<img src="https://i.postimg.cc/MpRK5GDQ/daily.png" width="1000">

<img src="https://i.postimg.cc/28gSnW4Y/rolling.png" width="1000">

<img src="https://i.postimg.cc/658Q7c4z/long.png" width="1000">

Something interesting about this platform is that it gives us a look at how it would perform in different economic, political and other scenarios. In this case, as the system does not cover such a long period of time, it only shows us the performance it could have had in the last crisis, that of the COVID-19 pandemic that occurred in 2020 and that affects us today.

<img src="https://i.postimg.cc/SQTsN3RJ/covid.png" width="1000">

To run this algorithm in a real broker and test it in the market, click on the Go live option and select your broker.

<img src="https://i.postimg.cc/R0bNNYVS/live.png" width="1000">

For the current degree project, with the 9 portfolios that we have for all profiles and for all horizons, we would only have to pay 740 dollars or a little more than $2.700. 000 Colombian pesos, for a fully automated system for a complete investment fund, this is undoubtedly a completely new paradigm, as it would leave out all types of analysts, traders, economists or financiers and all this work would be done by a machine, in this case the nodes, as mentioned above each algorithm must be in a node that will have available technological resources, each node is independent and the failure or change that is being done to an algorithm does not affect in any way to the other algorithms.

<img src="https://i.postimg.cc/rwXGpKZn/precio.png" width="250">

<img src="https://i.postimg.cc/TwFLH4Z7/precios-caracteristicas.png" width="800">

Finally comment that this system is completely accessible to all public, from the small retailer to large institutions, as mentioned above the 740 is for a complete fund with different profiles and horizons, for a particular profile with a single horizon this value does not reach 50 dollars, so a person with a capital of $ 5,000,000 Colombian pesos can cover the monthly costs for the system and be consistent with its portfolio over time fully automated.

In addition, you can have on the platform with the option to add people to the development team and try different tools, tests, techniques, among in a joint development, in addition, this system can be migrated to other brokerage platforms and be connected to different services through API.

<img src="https://i.postimg.cc/LXngDp0g/organizacion.png" width="1000">

I hope these instructions have been helpful. If you have any comments or suggestions you can send them to my Linkedin https://www.linkedin.com/in/juancardonasanchez/ 
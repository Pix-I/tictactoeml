from oxogame.NotSoSmartMachine import Not_So_Smart_Machine
import plotly.plotly as py
import plotly.graph_objs as go
import time
secondsArray = []

demo_machine = Not_So_Smart_Machine(5,3)
seconds = time.time()

for i in range(10):
    secondsArray.append(time.time()-seconds)
    demo_machine.smarter_play(100)
print(secondsArray)

arrayp = []
for i in range(1,9):
    arrayp.append(secondsArray[i] - secondsArray[i-1])
print(arrayp)
print(demo_machine.origin.moves)

trace0 = go.Scatter(
    x=[1, 2, 3, 4,5,6,7,8,9],
    y=demo_machine.fintesses
)
data = [trace0]

py.plot(data, filename = 'fitness', auto_open=False)

trace0 = go.Scatter(
    x=[1, 2, 3, 4,5,6,7,8,9],
    y=arrayp
)
data = [trace0]

py.plot(data, filename = 'timing', auto_open=True)



data = [go.Bar(
    x=[0,1, 2, 3, 4,5,6,7,8],
    y=demo_machine.origin.moves
)]

py.plot(data, filename = 'weights', auto_open=False)
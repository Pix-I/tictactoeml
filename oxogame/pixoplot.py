from oxogame.NotSoSmartMachine import Not_So_Smart_Machine
import plotly.plotly as py
import plotly.graph_objs as go
import time

config={'responsive': True}

def first_graphs():
    secondsArray = []
    demo_machine = Not_So_Smart_Machine(5, 3)
    seconds = time.time()
    for i in range(10):
        secondsArray.append(time.time() - seconds)
        demo_machine.dumber_play(100)
    print(secondsArray)
    arrayp = []
    for i in range(1, 9):
        arrayp.append(secondsArray[i] - secondsArray[i - 1])
    print(arrayp)
    print(demo_machine.origin.moves)
    trace0 = go.Scatter(
        x=[1, 2, 3, 4, 5, 6, 7, 8, 9],
        y=arrayp
    )
    data = [trace0]
    py.plot(data,config = config, output_type='div',
            include_plotlyjs='cdn',filename='timing', auto_open=True)
    data = [go.Bar(
        x=[0, 1, 2, 3, 4, 5, 6, 7, 8],
        y=demo_machine.origin.moves
    )]
    py.plot(data,config = config,output_type='div',
            include_plotlyjs='cdn', filename='weights', auto_open=True)


first_graphs()

def demo_play():
    demo_machine = Not_So_Smart_Machine(5, 3)
    result_set = []
    for i in range(8):
        demo_machine.dumber_play(1000)
        result_set.append(demo_machine.overal_fitness)
    trace0 = go.Scatter(
        x=[1, 2, 3, 4, 5, 6, 7, 8, 9],
        y=result_set
    )
    data = [trace0]
    py.plot(data,config = config, filename='demo_play', auto_open=True)


demo_play()

def random_fitness():
    fitness_machine = Not_So_Smart_Machine(5, 3)
    wins = []
    losses = []
    draws = []
    xgames = []
    for i in range(8):
        xgame = "{} simulations".format(100 * (i + 1))
        xgames.append(xgame)
        fitness_machine.dumber_play(100)
        wins.append(fitness_machine.total_victories)
        losses.append(fitness_machine.total_losses)
        draws.append(fitness_machine.total_draws)
        fitness_machine.reset_stats()
    print(fitness_machine.total_games_played)
    print(xgames)
    winsBar = go.Bar(
        x=xgames,
        y=wins,
        name='Wins'
    )
    drawsBar = go.Bar(
        x=xgames,
        y=draws,
        name='Draws'
    )
    lossesBar = go.Bar(
        x=xgames,
        y=losses,
        name='Losses'
    )
    data = [winsBar, drawsBar, lossesBar]
    layout = go.Layout(
        barmode='stack'
    )
    fig = go.Figure(data=data, layout=layout)
    py.plot(fig,config = config, filename='random_fitness')

def less_random_fitness():
    fitness_machine = Not_So_Smart_Machine(5, 3)
    wins = []
    losses = []
    draws = []
    xgames = []
    for i in range(8):
        xgame = "{} simulations".format(100 * (i + 1))
        xgames.append(xgame)
        fitness_machine.smarter_play(100)
        wins.append(fitness_machine.total_victories)
        losses.append(fitness_machine.total_losses)
        draws.append(fitness_machine.total_draws)
        fitness_machine.reset_stats()
    print(fitness_machine.total_games_played)
    print(xgames)
    winsBar = go.Bar(
        x=xgames,
        y=wins,
        name='Wins'
    )
    drawsBar = go.Bar(
        x=xgames,
        y=draws,
        name='Draws'
    )
    lossesBar = go.Bar(
        x=xgames,
        y=losses,
        name='Losses'
    )
    data = [winsBar, drawsBar, lossesBar]
    layout = go.Layout(
        barmode='stack'
    )
    fig = go.Figure(data=data, layout=layout)
    py.plot(fig,config = config, filename='less_random_fitness')


random_fitness()
less_random_fitness()


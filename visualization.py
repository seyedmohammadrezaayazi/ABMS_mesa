from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import ChartModule
import Model
from mesa.visualization.UserParam import UserSettableParameter


def portrayal(agent):
    if agent is None:
        return


# canvas_element = CanvasGrid(portrayal, 30, 30, 500, 500)
chart_element = ChartModule([{"Label": "total population", "Color": "#00008B"},
                             {"Label": "Men", "Color": "#00ff00"},
                             {"Label": "Women", "Color": "#FF00FF"},
                             {"Label": "Married Woman", "Color": "#fffc33"},
                             {"Label": "New Married Woman", "Color": "#7c7b79"},
                             {"Label": "Dead in the year", "Color": "#fc040b", }],
                            canvas_height=1100,
                            canvas_width=1300)

# "start_age": UserSettableParameter(
#     "slider", "Initial start age", 15, 12, 25
# ),

model_params = {
    "initial_man": UserSettableParameter(
        "slider", "Initial Man Population", 200000, 100000, 5000000, 10000
    ),
    "initial_woman": UserSettableParameter(
        "slider", "Initial Woman Population", 200000, 100000, 5000000, 10000
    ),
    "start_age_married": UserSettableParameter(
        "slider", "start age married", 21, 15, 25, 1
    ),
    "end_age": UserSettableParameter(
        "slider", "Initial end age", 49, 42, 70
    ),
    "evo_death": UserSettableParameter('choice', 'evo_death', value='last years',
                                       choices=['Exponential regression',
                                                'Combined regression',
                                                'Liner regression',
                                                'last years']),
    "initial_death_rate": UserSettableParameter(
        "slider", "Initial death rate", .5, 0.01, 1, 0.01
    ),
    "initial_evo_marriage": UserSettableParameter(
        "slider", "evo marriage", .4, 0.01, 1, 0.01
    ),
    "evo_brith": UserSettableParameter(
        "slider", "evo brith", .45, 0.01, 1, 0.01
    ),
    "last_years_marriage": UserSettableParameter(
        'number', ' last years marriage', value=5000)
    ,
    "reg_dead_a1": UserSettableParameter(
        'number', ' a1 in regression evo_death', value=9),
    "reg_dead_b": UserSettableParameter(
        'number', ' b in regression evo_death', value=250),
    "reg_dead_a2": UserSettableParameter(
        'number', ' a2 in regression evo_death', value=100)

}
server = ModularServer(
    Model.HumanModel, [chart_element],
    "Iran Demography simulation",
    model_params)
server.port = 1257


if __name__ == "__main__":
    server.launch()

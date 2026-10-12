#brp16_2

import stormpy

import pycarl

import stormpy.examples
import stormpy.examples.files

import stormpy._config as config


def example_parametric_models_01():
    # Check support for parameters
    if not config.storm_with_pars:
        print("Support parameters is missing. Try building storm-pars.")
        return

    import stormpy.pars
    path = stormpy.examples.files.prism_pdtmc_brp

    prism_program = stormpy.parse_prism_program(path)

    formula_str = "P<=0.1 [F (s = 5) & (r = 4) ]"

    
    # sto verificando che entrmabe nel futuro mutino in s = 4 ovvero in success e r =3 -> frame_reported

    properties = stormpy.parse_properties_for_prism_program(formula_str, prism_program)
    model = stormpy.build_parametric_model(prism_program, properties)

    initial_state = model.initial_states[0]


    # stampa della formula finale ottenibile

    result1 = stormpy.model_checking(model, properties[0])
    print("Result: {}".format(result1.at(initial_state)))

    print("Model supports parameters: {}".format(model.supports_parameters))
    parameters = model.collect_probability_parameters()


    print(parameters)
    assert len(parameters) == 2

    instantiator = stormpy.pars.PDtmcInstantiator(model)
    point = dict()

    
    for param in parameters:
        print(param.name)
        point[param] = stormpy.RationalRF("0.121213231") if param.name == "pL" else stormpy.RationalRF("0.7111211")

    # se voglio alta la probabilita' finale di ottenere il dado 5 
    # devo avera bassa p e bassa q perche' devo finire sempre negli archi 1-p e 1-q

    #for state in model.states:
        #print(state)
        #for action in state.actions:
            #for transition in action.transitions:
                #print(transition)
        
    # Recupero dei parametri di probabilità
    # parameters = model.collect_probability_parameters()
    
    # Creazione della regione
    # region = stormpy.Region() 

    # Aggiunta dei parametri alla regione con un intervallo di valori
    #for param in parameters:
        #region.add_interval_parameter(param, stormpy.Interval(0.2, 0.8))

    # Istantiazione del modello con i valori della regione
    # instantiator = stormpy.pars.PDtmcInstantiator(model)
    # instantiated_model = instantiator.instantiate_region(region)



    instantiated_model = instantiator.instantiate(point)
    result2 = stormpy.model_checking(instantiated_model, properties[0])
    
    
    # stampa dopo istanziazione dei parametri e risoluzione della formula     

    print(result2.at(initial_state))


if __name__ == '__main__':
    example_parametric_models_01()

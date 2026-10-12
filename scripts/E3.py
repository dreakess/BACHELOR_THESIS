import stormpy
import stormpy.info
import stormpy.dft as dft

import pycarl

import stormpy.examples
import stormpy.examples.files

import stormpy.pomdp

import stormpy._config as config


def pompd_analysis(t, k, op):
    # Check support for parameters
    if not config.storm_with_pars:
        print("Support parameters is missing. Try building storm-pars.")
        return

    import stormpy.pars as sp
    from pycarl.formula import FormulaType, Relation
    if stormpy.info.storm_ratfunc_use_cln():
        import pycarl.cln.formula
    else:
        import pycarl.gmp.formula

    # Prevent curious side effects from earlier runs (for tests only)
    pycarl.clear_variable_pool() 
    # ###
    # # How to apply an unknown FSC to obtain a pMC from a POMDP
    #path = stormpy.examples.files.prism_pomdp_maze
    path = "/home/paolo/Desktop/tesi/files/models/prova.prism"
    #print(path)
    prism_program = stormpy.parse_prism_program(path)

    threshold = t
    operator = str(op)
    fsc_k = k  

    # se k = 1 viene definito memoryless
    # se k = n allora viene definito con memoria finita k

    #formula_str = "P{}{} [true U<={} \"target\"]". format(operator, threshold, step)
    formula_str = "P{}{} [!\"bad\" U \"target\"]". format(operator, threshold)
    #formula_str = "P<0.6 [true U<30 \"target\"]"


    print(formula_str)

    # ovviamene stati di     goal e di bad vengono definiti all'interno del modello in Prism

    properties = stormpy.parse_properties_for_prism_program(formula_str, prism_program)
    # # construct the POMDP
    pomdp = stormpy.build_model(prism_program, properties)
    print(pomdp)
    # # make its representation canonic.
    pomdp = stormpy.pomdp.make_canonic(pomdp)
    print(pomdp)



    # Questa stampa serve a farmi capire se ho caricato correttamente il modello
    # e quindi ho una stampa per ogni stato, per ogni azione prob e stato raggiungente

    #stampa_stati_modello(pomdp)


    # # make the POMDP simple. This step is optional but often beneficial
    pomdp = stormpy.pomdp.make_simple(pomdp)
    # # construct the memory for the FSC
    # # in this case, a selective counter with two states
    memory_builder = stormpy.pomdp.PomdpMemoryBuilder()
    memory = memory_builder.build(stormpy.pomdp.PomdpMemoryPattern.selective_counter,fsc_k)
    # # apply the memory onto the POMDP to get the cartesian product
    pomdp = stormpy.pomdp.unfold_memory(pomdp, memory)
    # # apply the memory onto the POMDP to get the cartesian product
    



    pmc = stormpy.pomdp.apply_unknown_fsc(pomdp, stormpy.pomdp.PomdpFscApplicationMode.simple_linear)
    print(pmc)
    #stormpy.pars.simplify_model(pmc, formula_str)
    #print(pmc)



    export_options = stormpy.core.DirectEncodingOptions()
    export_options.allow_placeholders = True
    stormpy.export_to_drn(pmc, "test.out")


    #model = stormpy.build_parametric_model_from_drn("test.out")
    print("model from drn")
    #print(model)
 

    #model = stormpy.build_parametric_model(prism_program, properties)

    #initial_state = model.initial_states[0]


    # stampa della formula finale ottenibile


    #properties = stormpy.parse_properties_without_context(formula_str)
    
    #stampa_stati_modello(model)


    parameters = pmc.collect_probability_parameters()
    properties = stormpy.parse_properties_without_context("P=? [F \"goal\"]")

    region_formats = ""   
 

    import random

    i=0

    for x in parameters:
        i+=1
        #start = round(random.uniform(0, 1), 2)
        #end = round(random.uniform(start, 1), 2)
        #region_formats += str(start)+" <= "+str(x)+" <= " +str(end)+", "
        region_formats += "0.1 <= "+str(x)+ "<= 1.0, " # lascia 1.0 e non 1

    print(i)

    #region_string=list(region_formats)
    #print(region_string)
    #region_string.pop()
    #region_string1="".join(region_string)

    #print(region_string1)


    import stormpy.pars as spp
    stormpy.set_loglevel_error()


    env = stormpy.Environment()

    # settaggi per quanto riguarda l'analisi

    # posso settarli manualmente ma comunque anche se non settati vengono settati di default

    env.solver_environment.set_linear_equation_solver_type(stormpy.EquationSolverType.native)
    env.solver_environment.native_solver_environment.method = stormpy.NativeLinearEquationSolverMethod.gauss_seidel
    env.solver_environment.native_solver_environment.maximum_iterations = 5

    # qui abbiamo la creazione del checker che si occupa di istanziare la regione secondo il modello precedentemente creato
    # e la relativa formula (quella che ho definito sopra, ovvero voglio ritrovarmi in s7..)

    # print(properties[0].raw_formula)

    #


    #initial_state = model.initial_states[0]
    #print(initial_state)
    #collector = stormpy.ConstraintCollector(model)

    
    
    #region = spp.ParameterRegion.create_from_string(region_formats, model.collect_all_parameters())

    

    #checker = spp.create_region_checker(env, model, properties[0].raw_formula)


    
    bound = stormpy.RationalRF(threshold)
    # se scrivo Maximize allora sto dicendo: >, > =
    # se scrivo Minimize allora dico: <, <=

    # Pmax < 0.4  ?

    #print(IF_CENTER_SAT(checker, env , region=region_formats, f"P{operator}{threshold} [F \"goal\"]"))

    #result1 = stormpy.model_checking(model, properties[0])
    #print("Result: {}".format(result1.at(initial_state)))



    #if IF_CENTER_SAT(checker, env , region, formula_str): 
    #print("possiamo computare il result")
         # qui faccio la stampa dei valori che vengono dati ai parametri (in questo caso p e q)
    
    #print(best_case_result)
    #if operator == '>': direction = stormpy.OptimizationDirection.Maximize 
    #else: direction = stormpy.OptimizationDirection.Minimize

    #print(direction)

    #formula_str = "P"+operator+str(threshold)+" [F \"goal\"]"
    #properties = stormpy.parse_properties_without_context(formula_str.replace(operator, '=').replace(str(threshold), '?'))   
    #print(properties[0].raw_formula)
    #checker = spp.create_region_checker(env, model, properties[0].raw_formula)

    #best_case_result = checker.compute_extremum(env, region, direction, bound, precision_absolute = True)
        # qui faccio la stampa dei valori che vengono dati ai parametri (in questo caso p e q)
    
    #print(best_case_result)

    #print(str(best_case_result[0]) + " or approx " + str(float(best_case_result[0].constant_part())))
    #print(float(best_case_result[0].constant_part()) > 0.4) # P>0.5 [F s=7 & d=5]
    #else: 
      #  print("non e' possibile trovare una soluzione concreta")
    
    # qui viene calcolata la formula esatta 

    # exactSolution = stormpy.model_checking(model, properties[0])  
    # print(exactSolution)


    import subprocess

    print(str(t)+str(k)+op)
    output_file = 'output_test/P{}.txt'.format(str(t))

    # Construct the command as a single string
    command = (
    "/home/paolo/Desktop/storm/build/bin/storm-pars "
    "--mode feasibility "
    "--feasibility:method gd "
    "--explicit-drn /home/paolo/Desktop/tesi/files/scripts/test.out "
    f"--prop '{formula_str}' " 
    "--gradient-descent " 
    #"--termination-epsilon 1e-03 "
    "--smtsolver z3 "
    "--learning-rate 0.1 "  # Added a space after 0.1
    "-resources:tm "
    "--precision 0.1 "
    #"--exportbuild t.json "
    "--omit-inconsequential-params "
    "--descent-method plain " # di default viene messo l'adam
    "--batch-size 32 " # di default e' 32, gia' di per se questo valore e' ottimo per effettuare calcoli
    "--exact floats "
    f">> {output_file}"
)
    command2 = (
        "/home/paolo/Desktop/storm/build/bin/storm-pars "
        "--mode verification "
        "--explicit-drn /home/paolo/Desktop/tesi/files/scripts/test.out "
        f"--prop '{formula_str}' "
        "--regionbound 0.1 "
        "--exact floats "
        f">> {output_file}"
    )

    command3 = (
    "/home/paolo/Desktop/storm/build/bin/storm-pars "
    "--mode feasibility "
    "--feasibility:method pla "
    "--explicit-drn /home/paolo/Desktop/tesi/files/scripts/test.out "
    f"--prop '{formula_str}' "
    "--regionbound 0.1 "
    "--progress "
    "--smtsolver z3 "
    "--buildfull "
    #"--constants STEP_BOUND=1 "
    "--exact floats "
    "--trace "
    "--debug "
    "--additional-checks "
    f">> {output_file}"
)


    # Execute the command
    subprocess.run(command, shell=True)


    #import os 

    #args = [
    #"./storm-pars",
    #"--mode", "feasibility",
    #"--feasibility:method", "gd",
    #"--explicit-drn", "/home/paolo/Desktop/tesi/files/buoni/test.out",
    #"--prop", formula_str,
    #"--regionbound", "0.1"
    #"--smtsolver", "z3",
    #"--learning-rate", "0.1",
    ##"-resources:tm",   
    #]


    # ho messo regionbound perche' dato che non riesco a semplificare il modello generato, 
    # devo per forza dargli l'intervallo perche' altrimenti dovrei dargli anche tutte le variabile settate e questo
    # considera anche variabili che per conto della semplificazione non vengono considerate e ogni volta vengono generati 
    # i warning per sta cosa per ogni variabile non considerata nella semplificazione

    # ./storm-pars 
    # --mode feasibility 
    # --feasibility:method pla 
    # --explicit-drn /home/paolo/Desktop/tesi/files/buoni/test.out  
    # --prop 'Pmax>0.1 [!"bad" U "goal"]

    #os.execl("/home/paolo/Desktop/storm/build/bin/storm-pars", *args)
    

    # Generalmente i well formed constraints sono vincoli del tipo (-inf, 0]

    #print("Well formed constraints:")
    #for formula in collector.wellformed_constraints:
    #    print(formula.get_constraint())

    # I graph preserving constraints sono vincoli che inveve tendenzialmente anche se rapp. con '!='
    # sono vincoli di maggiore stretto quindi es. p-1 > 0

    #print("Graph preserving constraints:")
    #for formula in collector.graph_preserving_constraints:
    #    print(formula.get_constraint())


   
def stampa_stati_modello(model):
    for state in model.states:
        #if state.id in pomdp.initial_states:
         #   print("State {} is initial".format(state.id)) 
        for action in state.actions:
           for transition in action.transitions:
                print("From state {} by action {}, with probability {}, go to state {}".format(state, action, transition.value(), transition.column))


def IF_CENTER_SAT(checker, env, region):
    result = checker.check_region(env, region)
    # center sat  = 3 
    # center violated = 4
    print(result)
    return result.value == 3
        

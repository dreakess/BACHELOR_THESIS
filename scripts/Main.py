import E3


def main():

    threshold = 0.4
    k = 1
    step = 10

    
    #for k in range(1, 11):
    #    E3.pompd_analysis(t=0.2, k=k, op='>')

    #for k in range(4, 11):
    #    E3.pompd_analysis(t=0.3, k=k, op='>')


    #for k in range(1, 11):
    #    E3.pompd_analysis(t=0.33, k=k, op='>')

    #for k in range(1, 11):
    #    E3.pompd_analysis(t=0.39, k=k, op='>')

    #for k in range(1, 11):
    #    E3.pompd_analysis(t=0.4, k=k, op='>')
    
    #for k in range(1, 11):
    #    E3.pompd_analysis(t=0.5, k=k, op='>')

    #for k in range(1, 11):
    #    E3.pompd_analysis(t=0.56, k=k, op='>')

    #for k in range(1, 11):
    #    E3.pompd_analysis(t=0.6, k=k, op='>')

    #for k in range(1, 11):
    #    E3.pompd_analysis(t=0.7, k=k, op='>')

    for k in range(1, 11):
        E3.pompd_analysis(t=0.7, k=k, op='>')

    #E3.pompd_analysis(t=0.17, k=1, op='<')
    




    


if __name__ == '__main__':
    main()

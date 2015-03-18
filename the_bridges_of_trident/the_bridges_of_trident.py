# coding=utf-8

import Orange

def simple_instances(data, indexes=[5,7,40]):
    # przykładowe instancje
    for x in indexes:
        if x <= len(data):
            print x, ":", data[x]

def class_variable(data):
    # listę wartości zmiennej celu i histogram zmiennej celu
    from collections import Counter
    import numpy as np
    import matplotlib.mlab as mlab
    import matplotlib.pyplot as plt
    import pylab as plb


    items = Counter([d[data.domain.attributes[-1]].value for d in data if not d[data.domain.attributes[-1]].is_special()])
    print "Class variable values and counts:"
    print data.domain.attributes[-1].name
    for item in items.items():
        print "%-21s  : %4d" % item

    # generacja histogramu za pomocą matplotlib
    cm = plb.get_cmap('gist_rainbow')

    for index, item in enumerate(items):
        plt.bar(index+.1, item[1], label=item[0], color=cm(1.*index/len(items)))

    plt.xlabel('Group')
    plt.ylabel('Bridges')
    plt.axes().get_xaxis().set_visible(False)
    plt.title('Bridges by '+data.domain.classVar.name)
    plt.legend()

    plt.tight_layout()
    plt.show()


def attributes_names_and_types(data):
    # liczbę, nazwy i typy atrybutów z podziałem na atrybuty ciągłe i dyskretne
    a_Continuous = [x.name for x in data.domain.attributes if x.var_type==Orange.feature.Type.Continuous]
    a_Discrete = [x.name for x in data.domain.attributes if x.var_type==Orange.feature.Type.Discrete]
    print "%d attributes:" % len(data.domain.attributes)
    print "\t", len(a_Continuous), "continuous:", a_Continuous
    print "\t", len(a_Discrete), "discrete:", a_Discrete

def attributes_values(data):
    # wartości średnie (lub modalne) dla każdego atrybutu
    from collections import Counter

    average = lambda xs: sum(xs)/float(len(xs))

    print "%-15s %s" % ("Feature", "Mean or Mode")
    for x in data.domain.attributes:
        if x.var_type == Orange.feature.Type.Continuous:
            print "%-15s %.2f" % (x.name, average([d[x] for d in data if not d[x].is_special()]))
        if x.var_type == Orange.feature.Type.Discrete:
            print "%-15s %s" % (x.name, [d[0] for d in Counter([d[x].value for d in data if not d[x].is_special()]).most_common(1)])

def missing_values_count(data):
    # liczbę brakujących wartości dla każdego atrybutu
    print "Missing values count for each column:"
    for x in data.domain.features:
        n_miss = sum(1 for d in data if d[x].is_special())
        print "%6d %s" % (n_miss, x.name)

def small_instance_simple(data, procent = 10):
    # przykład niewielkiej próbki instancji
    import random
    import math

    print "random %d%% of original data:" % procent
    for d in random.sample(data, (int) (math.ceil((len(data)*procent)/100))):
        print d


def bridges_functions():
    data = Orange.data.Table("bridges")
    functions = [
                    simple_instances
                    ,
                    class_variable
                    ,
                    attributes_names_and_types
                    ,
                    missing_values_count
                    ,
                    attributes_values
                    ,
                    small_instance_simple
                ]
    for func in functions:
        print "\nFunction '%s':\n" % func.__name__
        func(data)

bridges_functions()

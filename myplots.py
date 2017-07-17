import matplotlib.pyplot as plt


def hist(dict):

    Sorted_Dict_Values = sorted(dict.values(), reverse=False)
    Sorted_Dict_Keys = sorted(dict, key=dict.get, reverse=False)
    for i in range(0,len(dict)):
        Key = Sorted_Dict_Keys[i]
        Sorted_Dict_Keys[i] = Key
    X = np.arange(Dictionary_Length)
    Colors = ('b','g','r','c')  # blue, green, red, cyan

    Figure = plt.figure()
    Axis = Figure.add_subplot(1,1,1)
    for i in range(0,Dictionary_Length):
        Axis.bar(X[i], Sorted_Dict_Values[i], align='center',width=0.5, color=Colors[i%len(Colors)])

    Axis.set_xticks(X)
    xtickNames = Axis.set_xticklabels(Sorted_Dict_Keys)
    plt.setp(Sorted_Dict_Keys)
    plt.xticks(rotation=20)
    ymax = max(Sorted_Dict_Values) + 1
    plt.ylim(0,ymax)

    plt.show()
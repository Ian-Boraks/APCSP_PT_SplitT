runNumber = 2
currentF = open('current_run.csv', 'a+')
time_list = [1, 2, 3, 4, 5,]

# currentF.writelines("run " + str(runNumber) + "\n")
for i in time_list:
    currentF.writelines(str(i) + ", run"  + str(runNumber) + "\n")
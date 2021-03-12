# Virtual Memory Project for 143b 
from vm import vmManager

if __name__ == "__main__":
    init = open("init-dp.txt","r").readlines() # type:list
    input_file = open("input-dp2.txt", "r").readlines()
    output_file = open("output.txt", "w")

    # 1. process the init file and input file contents
    for i,line in enumerate(init):
        init[i] = [int(j) for j in line.split()]
    line1, line2 = [],[]
    for i in range(0,len(init[0]),3):
        entry = []
        entry.append(init[0][i])
        entry.append(init[0][i+1])
        entry.append(init[0][i+2])
        line1.append(entry)
    for i in range(0,len(init[1]),3):
        entry = []
        entry.append(init[1][i])
        entry.append(init[1][i+1])
        entry.append(init[1][i+2])
        line2.append(entry)
    input_file = [int(i) for i in input_file[0].split()]
        
    # 2. initialize the VA
    vm = vmManager(line1,line2,input_file)
    vm.initialization()

    # 3. Translate VA->PA and write to the output file
    vm.tran_VA()
    result = vm.output()
    output_file.write(result)
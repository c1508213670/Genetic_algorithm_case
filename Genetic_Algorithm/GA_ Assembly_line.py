import random
import copy
import pandas as pd

from texttable import Texttable


def calculate_cmax(n,m,t_matrix,individual):
    c_max=0
    for i in range(n):
        for j in range(m):
            if i!=0:
                temp1=calculate_cmax(i,j+1,t_matrix,individual)
                temp2= calculate_cmax(i+1,j,t_matrix,individual)
                if temp1 < temp2:
                    c_max=temp2+t_matrix[individual[i]-1][j]
                else:
                    c_max=temp1+t_matrix[individual[i]-1][j]
            else:
                c_max+=t_matrix[individual[i]-1][j]
    return c_max



def Factorial(n):
    if n==0:
        return 1
    elif n>0:
        temp=1
        for i in range(n):
            temp*=(i+1)
        return temp
    else:
        return 0

def Create_Initial_population(n,individual_num):
    ls=[i+1 for i in range(n)]
    individual_ls=[]
    individual_count=0
    max_count=Factorial(n)
    while individual_count!=individual_num:
        temp=ls[:]
        random.shuffle(temp)
        if temp not in  individual_ls:
            individual_ls.append(temp)
            individual_count+=1
        if individual_count >= max_count:
            break
    return individual_ls

def Fitness(c_max):
    return 1/c_max

def Selection(n,m,t_matrix,individual_ls):
    temp_ls=copy.deepcopy(individual_ls)
    sum_fitness=0
    sum_per_fitness=0
    new_individual_ls=[]
    for i in range(len(temp_ls)):
        temp=calculate_cmax(n,m,t_matrix,temp_ls[i])
        temp_ls[i]=[temp_ls[i],Fitness(temp)]
        sum_fitness+=Fitness(temp)
    for i in range(len(temp_ls)):
        temp=temp_ls[i][1]/sum_fitness
        temp_ls[i].append(temp)
        sum_per_fitness+=temp
        temp_ls[i].append(sum_per_fitness)
    # print(temp_ls)
    min_individual=temp_ls[0][0]
    max_individual=temp_ls[0][0]
    cal_sum=0
    cal_avg=0
    min_coun=0
    for i in range(len(temp_ls)-1):
        temp=random.random()
        for j in range(len(temp_ls)):
            if temp_ls[j][3]-temp_ls[j][2] <= temp and temp_ls[j][3] > temp:
                new_individual_ls.append(individual_ls[j])
                break
    for i in range(len(temp_ls)):
        if calculate_cmax(n,m,t_matrix,temp_ls[i][0]) < calculate_cmax(n,m,t_matrix,min_individual):
            min_individual=temp_ls[i][0][:]
    for i in range(len(temp_ls)):
        if calculate_cmax(n,m,t_matrix,temp_ls[i][0]) > calculate_cmax(n,m,t_matrix,max_individual):
            max_individual=temp_ls[i][0][:]
    for i in range(len(temp_ls)):
        cal_sum+=calculate_cmax(n,m,t_matrix,temp_ls[i][0])
    cal_avg+=(cal_sum/len(temp_ls))
    new_individual_ls.append(min_individual)
    return new_individual_ls,min_individual,max_individual,cal_avg

def Overlapping(pro,individual_ls):
    for i in range(len(individual_ls)//2):
        if random.random() <= pro:
            left=random.randint(0,len(individual_ls)//2-1)
            right=random.randint(len(individual_ls)//2,len(individual_ls)-1)
            temp_ls1=individual_ls[i][left:right+1]
            temp_ls2=[]
            count=0
            # print(individual_ls[i],individual_ls[len(individual_ls)//2+i])
            for j in range(len(individual_ls[len(individual_ls)//2+i])):
                if individual_ls[len(individual_ls)//2+i][j] in temp_ls1:
                    temp_ls2.append(individual_ls[len(individual_ls)//2+i][j])
                    individual_ls[len(individual_ls)//2+i][j]=temp_ls1[count]
                    count+=1
            count=0
            for j in range(len(individual_ls[i])):
                if individual_ls[i][j] in temp_ls2:
                    individual_ls[i][j]=temp_ls2[count]
                    count+=1
            # print(temp_ls1,temp_ls2,individual_ls[i],individual_ls[len(individual_ls)//2+i])
    return individual_ls
def Variation(pro,individual_ls):
    for i in range(len(individual_ls)):
        if random.random() < pro:
            if len(individual_ls[i]) > 1:
                left=random.randint(0,len(individual_ls[i])//2-1)
                right=random.randint(len(individual_ls[i])//2,len(individual_ls[i])-1)
                temp=individual_ls[i][left]
                individual_ls[i][left]=individual_ls[i][right]
                individual_ls[i][right]=temp
    return individual_ls

def main(t_matrix,n,m,individual_num,o_pro,v_pro,all_num,iterations_nums):
    final_data_ls=[]
    print("当前运行次数：")
    print(iterations_nums)

    for w in range(iterations_nums):
        cal_avg_sum=0
        best_count=0
        best_ls=[]
        individual_ls=Create_Initial_population(n,individual_num)
        print("当前迭代次数：")
        print(all_num)
        print("初始种群:")
        print(individual_ls)
        final_data=[]
        max_individual=[]
        min_individual=[]
        s_individual_ls=Selection(n,m,t_matrix,individual_ls)
        # print("选择：")
        # print(s_individual_ls[0])
        min_individual=s_individual_ls[1][:]
        max_individual=s_individual_ls[2][:]
        cal_avg_sum+=s_individual_ls[3]
        o_individual_ls=Overlapping(o_pro,s_individual_ls[0])
        # print("交叉：")
        # print(o_individual_ls)
        v_individual_ls=Variation(v_pro,o_individual_ls)
        # print("变异：")
        # print(v_individual_ls)

        for i in range(all_num):
            s_individual_ls=Selection(n,m,t_matrix,v_individual_ls)
            # print("选择：")
            # print(s_individual_ls[0])
            best_ls.append(s_individual_ls[1][:])
            if calculate_cmax(n,m,t_matrix,s_individual_ls[1]) < calculate_cmax(n,m,t_matrix,min_individual):
                min_individual=s_individual_ls[1][:]
            if calculate_cmax(n,m,t_matrix,s_individual_ls[2]) > calculate_cmax(n,m,t_matrix,max_individual):
                max_individual=s_individual_ls[2][:]
            cal_avg_sum+=s_individual_ls[3]
            o_individual_ls=Overlapping(o_pro,s_individual_ls[0])
            # print("交叉：")
            # print(o_individual_ls)
            v_individual_ls=Variation(v_pro,o_individual_ls)
            # print("变异：")
            # print(v_individual_ls)
        cal_avg_sum=cal_avg_sum/(all_num+1)
        for i in range(len(best_ls)):
            if best_ls[i]==min_individual:
                best_count=i
                break
        final_data.append(calculate_cmax(n,m,t_matrix,min_individual))
        final_data.append(calculate_cmax(n,m,t_matrix,max_individual))
        final_data.append(cal_avg_sum)
        final_data.append(best_count)
        print("结果列表为：（依次对应：最好解，最坏解，平均解，最好接最早出现迭代数）")
        print(final_data)
        final_data_ls.append(final_data)
    print(final_data_ls)
    res_ls=[]
    res_ls.append(iterations_nums)
    best_cal=final_data_ls[0][0]
    worst_cal=final_data_ls[0][1]
    sum_avg_cal=0
    best_fre_count=0
    for i in range(len(final_data_ls)):
        if best_cal > final_data_ls[i][0]:
            best_cal=final_data_ls[i][0]
        if worst_cal < final_data_ls[i][1]:
            worst_cal=final_data_ls[i][1]
        sum_avg_cal+=final_data_ls[i][2]
        best_fre_count+=final_data_ls[i][3]
    sum_count=0
    for i in range(len(final_data_ls)):
        if final_data_ls[i][0]==best_cal:
            sum_count+=1
    sum_count_per=sum_count/len(final_data_ls)
    sum_avg_cal=sum_avg_cal/(len(final_data_ls))
    best_fre_count=best_fre_count/(len(final_data_ls))
    res_ls.append(best_cal)
    res_ls.append(worst_cal)
    res_ls.append(sum_avg_cal)
    res_ls.append(sum_count_per)
    res_ls.append(best_fre_count)
    colums=["总运行次数","最好解","最坏解","平均解","最好解的频率","最好的平均迭代次数"]
    df=pd.DataFrame([res_ls],columns=colums,index=[1])
    # print("结果表")
    # print(df)
    tb=Texttable()
    tb.set_cols_align(['l','r','r','r','l','l'])
    tb.set_cols_dtype(['i','f','f','f','f','f'])
    tb.header(df.columns)
    tb.add_rows(df.values,header=False)
    print(tb.draw())

#参数说明
# t_matrix:流水线矩阵 n：行 m：列
# individual_num：种群个数 o_pro:交叉概率 v_pro:变异概率
# all_nums:迭代次数 iterations_nums:运行次数

if __name__ == '__main__':
    t_matrix=[[31,41,25,30],[19,55,3,34],[23,42,27,6],[13,22,14,13],[33,5,57,19]]
    n=5
    m=4
    idividual_num=20
    o_pro=0.6
    v_pro=0.1
    all_num=30
    iterations_nums=20
    main(t_matrix,n,m,idividual_num,o_pro,v_pro,all_num,iterations_nums)


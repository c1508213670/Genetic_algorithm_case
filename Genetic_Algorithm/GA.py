import random
import math
import copy
import pandas as pd
from texttable import Texttable
#计算编码数位
def Count_power_of_two(num):
    temp_count=0
    flag=0
    while num//2!=0 :
        temp_count+=1
        num=num//2
    return temp_count + 1

#计算十进制值
#@param  individual_ls 二进制列表
# l_limit 下限值
#@return 十进制的值

def Binary_to_decimalism(individual_ls,l_limit):
    sum=0
    for i in range(len(individual_ls)):
        sum+=individual_ls[len(individual_ls)-1-i]*pow(2,i)
    sum=sum/100
    sum+=l_limit
    return sum

#创建初始编码随机种群
#@param
#l_limit 区间下限
#u_limit 区间上限
#num 需要生成的个体数量
#demical_digit=0 小数点精确位数
#Interval=0 开闭情况，全闭为0，全开为1
#@return 随机个体列表

def Create_individual_ls(l_limit,u_limit,num,demical_digit=0,Interval=0):
    temp_section_sum=(u_limit-l_limit-Interval)*pow(10,demical_digit)
    temp_count=Count_power_of_two(temp_section_sum)
    individual_ls=[]
    sum_individual_ls=u_limit+1
    while len(individual_ls)!=num:
        singal_individual_ls=[]
        sum_individual_ls=u_limit+1
        while sum_individual_ls >= u_limit or sum_individual_ls <= l_limit:
            singal_individual_ls=[]
            for i in range(temp_count):
                singal_individual_ls.append(random.randint(0,1))
            sum_individual_ls=Binary_to_decimalism(singal_individual_ls,l_limit)
        if singal_individual_ls not in individual_ls:
            individual_ls.append(singal_individual_ls)
    # for i in individual_ls:
        # print(i)
        # print(Binary_to_decimalism(i,l_limit))
    return individual_ls

#计算适应度
#@param sigal_individual_ls 单个个体染色体
#适应度函数 需要根据求值的不同调整
#eg:y=10*sin(5*x)+7*abs(x-5)+10
#求最大值 适应度函数为 该方程
#求最小值 适应度函数 为方程分之一
def Fitness(sigal_individual_ls,l_limit):
    temp=Binary_to_decimalism(sigal_individual_ls,l_limit)
    return 10*math.sin(temp*5)+7*math.fabs(temp-5)+10

def Selection(individual_ls,l_limit,worst_individual=0,best_individual=0):
    if best_individual==0:
        temp_ls=individual_ls[:]
        sum_fitness=0
        roulette_pro=0
        best_person_no=0
        best_person_fitness=0
        worst_person_no=0
        worst_person_fitness=0
        for i in range(len(temp_ls)):
            temp=Fitness(temp_ls[i],l_limit)
            sum_fitness+=temp
            temp_ls[i]=[temp_ls[i],temp]
            if best_person_fitness < temp:
                best_person_no=i
                best_person_fitness=temp
            if worst_person_fitness > temp:
                worst_person_no=i
                worst_person_fitness=temp
        for i in range(len(temp_ls)):
            pro=temp_ls[i][1]/sum_fitness
            roulette_pro+=pro
            temp_ls[i]=[temp_ls[i][0],temp_ls[i][1],pro,roulette_pro,0]

        temp_ls[best_person_no][4]+=1
        best_individual=temp_ls[best_person_no][0]
        worst_individual=temp_ls[worst_person_no][0]

        for i in range(len(temp_ls)-1):
            temp=random.random()
            for j in range(len(temp_ls)):
                if temp < temp_ls[j][3] and temp >= temp_ls[j][3]-temp_ls[j][2] :
                    temp_ls[i][4]+=1
                    break
        return temp_ls,best_individual,worst_individual
    else:
        temp_ls=individual_ls[:]
        sum_fitness=0
        roulette_pro=0
        best_person_no=0
        best_person_fitness=0
        worst_person_no=0
        worst_person_fitness=Fitness(temp_ls[0],l_limit)
        for i in range(len(temp_ls)):
            temp=Fitness(temp_ls[i],l_limit)
            sum_fitness+=temp
            temp_ls[i]=[temp_ls[i],temp]
            if best_person_fitness < temp:
                best_person_no=i
                best_person_fitness=temp
            if worst_person_fitness > temp:
                worst_person_no=i
                worst_person_fitness=temp
        for i in range(len(temp_ls)):
            pro=temp_ls[i][1]/sum_fitness
            roulette_pro+=pro
            temp_ls[i]=[temp_ls[i][0],temp_ls[i][1],pro,roulette_pro,0]

        for i in range(len(temp_ls)-1):
            temp=random.random()
            for j in range(len(temp_ls)):
                if temp < temp_ls[j][3] and temp > temp_ls[j][3]-temp_ls[j][2] :
                    temp_ls[i][4]+=1
                    break

        if Fitness(temp_ls[worst_person_no][0],l_limit) < Fitness(worst_individual,l_limit):
            worst_individual=temp_ls[worst_person_no][0]

        if Fitness(temp_ls[best_person_no][0],l_limit) < Fitness(best_individual,l_limit):
            temp_ls[worst_person_no][0]=best_individual
            temp_ls[worst_person_no][4]+=1
            # print("best_individual",Binary_to_decimalism(best_individual,l_limit),Fitness(best_individual,l_limit))
        else:
            temp_ls[best_person_no][4]+=1
            best_individual=temp_ls[best_person_no][0]
            # print("best_individual",Binary_to_decimalism(best_individual,l_limit),Fitness(best_individual,l_limit))
        return temp_ls,best_individual,worst_individual

def Exchange_chromosome_avr(ls1,ls2):
    temp_individual_ls=[]
    for i in range(len(ls1)):
        temp_individual_ls.append(random.randint(0,1))
    for i in range(len(temp_individual_ls)):
        if temp_individual_ls[i] == 1:
            temp=ls1[i]
            ls1[i]=ls2[i]
            ls2[i]=temp
    return ls1,ls2


def Exchange_chromosome_part(ls1,ls2,section_size,l_limit):
    temp=len(ls1)-1
    ls1_temp=ls1[:]
    ls2_temp=ls2[:]
    l_change_position=random.randint(0,temp//2)
    h_change_position=random.randint(temp//2,temp)
    ls1_change_part=ls1[l_change_position:h_change_position]
    ls2_change_part=ls2[l_change_position:h_change_position]
    for i in range(len(ls1_change_part)):
        ls2[l_change_position+i]=ls1_change_part[i]
    for i in range(len(ls2_change_part)):
        ls1[l_change_position+i]=ls2_change_part[i]
    while Binary_to_decimalism(ls2,l_limit)>=section_size or Binary_to_decimalism(ls1,l_limit)>=section_size:
        l_change_position=random.randint(0,temp//2)
        h_change_position=random.randint(temp//2,temp)
        ls1_change_part=ls1_temp[l_change_position:h_change_position]
        ls2_change_part=ls2_temp[l_change_position:h_change_position]
        for i in range(len(ls1_change_part)):
            ls2[l_change_position+i]=ls1_change_part[i]
        for i in range(len(ls2_change_part)):
            ls1[l_change_position+i]=ls2_change_part[i]
    return ls1,ls2

def Overlapping (selection_ls,section_size,l_limit):
    temp_ls=[]
    temp_sum=0
    i=0
    while temp_sum != len(selection_ls):
        if selection_ls[i][4] != 0:
            for j in range(selection_ls[i][4]):
                temp_ls.append(selection_ls[i][0])
                temp_sum+=1
        i+=1
    random.shuffle(temp_ls)
    for i in range(len(temp_ls)//2):
        if random.random()<0.5:
            Exchange_chromosome_part(temp_ls[i],temp_ls[len(temp_ls)//2+i],section_size,l_limit)
    return temp_ls

def Illegal_check(ols,section_size,l_limit):
    for i in ols:
        if Binary_to_decimalism(i,l_limit) >= section_size:
            return 1
    return 0

def Variation(ols,section_size,l_limit,force_change_factor=0.01):
    temp_force_ls=[]
    ols_temp=copy.deepcopy(ols)
    for i in range(len(ols[0])):
        temp_force_ls.append([])
    for i in range(len(ols)):
        for j in range(len(ols[i])):
            temp_force_ls[j].append(ols[i][j])
            if random.random()<0.003:
                if ols[i][j]==1:
                    ols[i][j]=0
                else:
                    ols[i][j]=1
                # print("Variation!")
    # print(temp_force_ls)
    temp_target_ls=[]
    r=random.random()
    if r<force_change_factor:
        for i in range(len(temp_force_ls)):
            flag=1
            temp=temp_force_ls[i][0]
            for j in temp_force_ls[i]:
                if temp!=j:
                    flag=0
                    break
            if flag==1:
                temp_target_ls.append([i,temp_force_ls[i]])
        # print(temp_target_ls)
        for i in range(len(temp_target_ls)):
            if random.random()<0.5:
                temp=random.randint(0,len(ols)-1)
                temp_random_posotion=random.randint(0,len(temp_target_ls)-1)
                # print(temp)
                if ols[temp][temp_target_ls[temp_random_posotion][0]]==1:
                    ols[temp][temp_target_ls[temp_random_posotion][0]]=0
                else:
                    ols[temp][temp_target_ls[temp_random_posotion][0]]=1
                # print("fVariation!")
    while Illegal_check(ols,section_size,l_limit):
        temp_force_ls=[]
        for i in range(len(ols_temp[0])):
            temp_force_ls.append([])
        for i in range(len(ols_temp)):
            for j in range(len(ols_temp[i])):
                temp_force_ls[j].append(ols_temp[i][j])
                if random.random()<0.003:
                    if ols[i][j]==1:
                        ols[i][j]=0
                    else:
                        ols[i][j]=1
                    # print("Variation!")
        # print(temp_force_ls)
        temp_target_ls=[]
        r=random.random()
        if r < force_change_factor:
            for i in range(len(temp_force_ls)):
                flag=1
                temp=temp_force_ls[i][0]
                for j in temp_force_ls[i]:
                    if temp!=j:
                        flag=0
                        break
                if flag==1:
                    temp_target_ls.append([i,temp_force_ls[i]])
            # print(temp_target_ls)
            for i in range(len(temp_target_ls)):
                if random.random()<0.5:
                    temp=random.randint(0,len(ols)-1)
                    temp_random_posotion=random.randint(0,len(temp_target_ls)-1)
                    # print(temp)
                    if ols[temp][temp_target_ls[temp_random_posotion][0]]==1:
                        ols[temp][temp_target_ls[temp_random_posotion][0]]=0
                    else:
                        ols[temp][temp_target_ls[temp_random_posotion][0]]=1
                    # print("fVariation!")
    return ols

def find_spcial_individual(individual_ls,l_limit):
    fitness_dict=dict({})
    worst_individual=[]
    best_individual=[]
    sum_fitness=0
    avg_fitness=0
    for i in individual_ls:
        if Binary_to_decimalism(i,l_limit) not in fitness_dict:
            fitness_dict[Binary_to_decimalism(i,l_limit)] = Fitness(i,l_limit)
        sum_fitness+=Fitness(i,l_limit)
    avg_fitness=sum_fitness/len(individual_ls)
    for key,value in fitness_dict.items():
        if(value == max(fitness_dict.values())):
            for i in individual_ls:
                if Binary_to_decimalism(i,l_limit)==key:
                    best_individual=i
                    break
        if (value == min(fitness_dict.values())):
            for i in individual_ls:
                if Binary_to_decimalism(i,l_limit)==key:
                    worst_individual= i
                    break
    return best_individual,worst_individual,avg_fitness

def do_sov(n,l_limit,u_limit,num,demical_digit=0,Interval=0):
    print("迭代次数为：")
    print(n)
    flag=0
    repeat_time=0
    best_individual_count=0
    worst_individual_count=0
    best_individual=[]
    worst_individual=[]
    best_n=0
    all_best_individual_ls=[]
    all_worst_individual_ls=[]
    all_avg_individual_ls=[]
    ls=Create_individual_ls(l_limit,u_limit,num,demical_digit,Interval)
    #print(ls)
    sls_tuple=Selection(ls,0)
    sls=sls_tuple[0]
    #print(sls)
    best_individual=copy.deepcopy(sls_tuple[1])
    worst_individual=copy.deepcopy(sls_tuple[2])
    ols=Overlapping(sls,10,l_limit)
    #print(ols)
    vls=Variation(ols,10,l_limit)
    # print(vls)
    for i in range(n):
        sls_tuple=Selection(vls,0,worst_individual,best_individual)
        sls=sls_tuple[0]
        best_individual=copy.deepcopy(sls_tuple[1])
        worst_individual=copy.deepcopy(sls_tuple[2])
        ols=Overlapping(sls,10,l_limit)
        if flag==0:
            repeat_time+=1
            vls=Variation(ols,10,l_limit)
            # print(vls)
            individual_tuple=find_spcial_individual(vls,l_limit)
            all_worst_individual_ls.append(individual_tuple[1])
            all_best_individual_ls.append(individual_tuple[0])
            all_avg_individual_ls.append(individual_tuple[2])
            local_optimum_count=0
            for i in range(len(all_best_individual_ls)):
                if all_best_individual_ls[i]==individual_tuple[0]:
                    local_optimum_count+=1
            if local_optimum_count > 3 and repeat_time > 1:
                flag=1
            else:
                flag=0
            # print(Binary_to_decimalism(individual_tuple[0],l_limit))
            # print(Fitness(individual_tuple[0],l_limit))
            # print(Binary_to_decimalism(individual_tuple[1],l_limit))
            # print(individual_tuple[2])
        else:
            vls=Variation(ols,10,l_limit,0.5)
            repeat_time=0
            # print(vls)
            individual_tuple=find_spcial_individual(vls,l_limit)
            all_worst_individual_ls.append(individual_tuple[1])
            all_best_individual_ls.append(individual_tuple[0])
            all_avg_individual_ls.append(individual_tuple[2])
            flag=0
            # print(Binary_to_decimalism(individual_tuple[0],l_limit))
            # print(Fitness(individual_tuple[0],l_limit))
            # print(Binary_to_decimalism(individual_tuple[1],l_limit))
            # print(individual_tuple[2])
    for i in range(len(all_best_individual_ls)):
        if all_best_individual_ls[i]==best_individual:
            best_individual_count+=1
            if best_individual_count==1:
                best_n=i
    for i in range(len(all_worst_individual_ls)):
        if all_worst_individual_ls[i]==worst_individual:
            worst_individual_count+=1
    sum_avg=0
    for i in range(len(all_avg_individual_ls)):
        sum_avg+=all_avg_individual_ls[i]
    avg_fitness=sum_avg/len(all_avg_individual_ls)
    data=[Fitness(best_individual,l_limit),Fitness(worst_individual,l_limit),avg_fitness,best_n]
    print("结果列表为：（依次对应：最好解，最坏解，平均解，最好接最早出现迭代数）")
    print(data)
    return data

def main():
    n_executions=20 #执行次数
    n=30 #迭代次数
    l_limit=0 #下限
    u_limit=10 #上限
    num=6 #种群大小
    demical_digit=2 #小数点位数
    Interval=0 #是否开闭（详情见上文
    best_individual_fitness_ls=[]
    worst_individual_fitness_ls=[]
    avg_fitness_ls=[]
    best_frequency=0
    best_no_ls=[]
    final_data=[]
    print("执行次数：")
    print(n_executions)
    for i in range(n_executions):
        data=do_sov(n,l_limit,u_limit,num,demical_digit,Interval)
        best_individual_fitness_ls.append(data[0])
        worst_individual_fitness_ls.append(data[1])
        avg_fitness_ls.append(data[2])
        best_no_ls.append(data[3])
    best_fitness=max(best_individual_fitness_ls)
    final_data.append(n_executions)
    final_data.append(best_fitness)
    final_data.append(min(worst_individual_fitness_ls))
    best_fitness_count=0
    final_data.append(sum(avg_fitness_ls)/len(avg_fitness_ls))
    for i in best_individual_fitness_ls:
        if best_fitness==i:
            best_fitness_count+=1
    best_frequency=best_fitness_count/len(best_individual_fitness_ls)
    final_data.append(best_frequency)
    final_data.append(sum(best_no_ls)/len(best_no_ls))
    colums=["总运行次数","最好解","最坏解","平均解","最好解的频率","最好的平均迭代次数"]
    df=pd.DataFrame([final_data],columns=colums,index=[1])
    # print("结果表")
    # print(df)
    tb=Texttable()
    tb.set_cols_align(['l','r','r','r','l','l'])
    tb.set_cols_dtype(['i','f','f','f','f','f'])
    tb.header(df.columns)
    tb.add_rows(df.values,header=False)
    print(tb.draw())

if __name__ == '__main__':
    main()


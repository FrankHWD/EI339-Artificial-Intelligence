edges=[[1,2],[1,3],[2,4],[3,6],[4,7],[7,8],[8,9],[6,10],[9,10],[2,3],[2,5],[4,5],[3,5],[5,6],[4,8],[5,8],[5,9],[6,9]]
table=[]

def addscore(point):
    x=point[0]
    y=point[1]
    s=0
    for i in range(1,11):
        if ([x,i] in table or [i,x] in table) and ([y,i] in table or [i,y] in table):
            s+=1  #if (x,t) and (y,t) is already in the drawn set,then the new edge(x,y) will form a new traingle
    return s

def minimax_value(types,remain_lines,alpha,beta):
    if len(remain_lines)==1:
        v=addscore(remain_lines[0])
        return v*types
    if types==1:
        v=-1000
        for i in range(len(remain_lines)):
            table.append(remain_lines[i])
            new_remain_lines=remain_lines.copy()
            new_remain_lines.remove(remain_lines[i])
            score=addscore(remain_lines[i])
            flag=-1 #if the outcome is 0, it will becomes the  playerA's turn
            if score>0: #if the outcome is positive, it will still be the playerA's tuen
                flag=1
            v=max(v,minimax_value(flag,new_remain_lines,alpha,beta)+score)
            table.remove(remain_lines[i])
            if v>=beta:
                return v
            alpha=max(alpha,v)
        return v
    elif types==-1:
        v=1000
        for i in range(len(remain_lines)):
            new_remain_lines=remain_lines.copy()
            new_remain_lines.remove(remain_lines[i])
            score=addscore(remain_lines[i])
            table.append(remain_lines[i])
            flag=-1  #if the outcome is negative, it will still be the playerB's tuen
            if score==0: #if the outcome is 0, it will becomes the  playerA's turn
                flag=1
            v=min(v,minimax_value(flag,new_remain_lines,alpha,beta)-score)
            table.remove(remain_lines[i])
            if v<=alpha:
                return v
            beta=min(beta,v)
        return v

if __name__=='__main__':
    print("Please input:")
    table = []
    line = input()
    lines = line.split()
    res=0
    flag=1
    for item in lines:
        score=addscore([int(item[1]),int(item[3])])
        table.append([int(item[1]), int(item[3])])
        if flag>0:
            res+=score
        else:
            res+=-score
        if score==0:
            flag=-flag
    remainline=[item for item in edges if item not in table]
    value=minimax_value(flag,remainline,-100,100)
    res+=value
    if res>0:
        print("A win!")
    elif res<0:
        print("B win!")
    else:
        print("Draw!")
from functools import lru_cache

def valid_move(n,x,y):
    if 0<x and x<n+1 and 0<y and y<n+1:
        return 1
    return 0

@lru_cache(None)
def minimax_value(n,types,x1,y1,x2,y2,depth):
    if x1==x2 and y1==y2:
        res=-types*30-depth
        return res
    elif depth>4*n:
        res=-4*n-1
        return res
    if types==1:
        v=-1000
        next=[[x1-1,y1-1],[x1-1,y1],[x1-1,y1+1],[x1,y1-1],[x1,y1+1],[x1+1,y1-1],[x1+1,y1],[x1+1,y1+1]]
        for i in range(8):
            if valid_move(n,next[i][0],next[i][1]):
                v=max(v,minimax_value(n,-1,next[i][0],next[i][1],x2,y2,depth+1))
        return v
    elif types==-1:
        v=1000
        next=[[x2-1,y2],[x2,y2-1],[x2,y2+1],[x2+1,y2]]
        for i in range(4):
            if valid_move(n, next[i][0], next[i][1]):
                v=min(v,minimax_value(n,1,x1,y1,next[i][0],next[i][1],depth+1))
        return v

if __name__=='__main__':
    print("Please input:")
    line = input()
    lines = line.split()
    n = int(lines[0])
    r1 = int(lines[1])
    c1 = int(lines[2])
    r2 = int(lines[3])
    c2 = int(lines[4])
    if abs(r1-r2)+abs(c1-c2)==1:
        print("WHITE",1)
    else:
        result=30-minimax_value(n,-1,r1,c1,r2,c2,0)
        print("BLACK",result)

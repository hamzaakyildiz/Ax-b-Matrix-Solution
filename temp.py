
from copy import copy, deepcopy

def multiplyMatrices(A,b):
    r=[]
    if len(A)==1:
        r.append(A[0]*b[0])
        return r
    r=[0]*len(A)
    for i in range(len(A)):
        for j in range(len(A)):
            r[i]+=A[i][j]*b[j]

    return r

def exchangeRows(M,firstRow,secondRow):
    temp=M[firstRow][:]
    M[firstRow][:]=M[secondRow][:]
    M[secondRow][:]=temp
    
def multiplyRow(M,nonZeroConstant,rowNumber):
    for i in range(len(M[rowNumber])):
        M[rowNumber][i]=M[rowNumber][i]*nonZeroConstant
        
def multiplyMatrix(M, c):
    for i in range(len(M)):
        multiplyRow(M, c, i)
        
def rowOperationRow(M,firstRow,secondRow,c):
    for i in range(len(M[firstRow])):
        M[firstRow][i]=M[firstRow][i]+M[secondRow][i]*c
        
def printArr(M):
    for i in range(len(M)):
        for j in range(len(M[i])):
            print("{:.3f}".format(M[i][j]),end =" "),
        print() 
    print()    
    
def rank(M):
    v=deepcopy(M)
    pivoting(v)
    rank = 0
    for i in range(len(v)):
        for j in range(len(v[i])):
            if v[i][j]!=0:
                rank +=1
                break
    return rank 

def pivoting(M):
    n=len(M)
    for row in range(0,n):
        col=row
        k=[]
        if M[row][col]==0:
            for j in range(row+1,n):
                if M[j][col]!=0:
                    exchangeRows(M, j, row)
                    break
        if M[row][col] == 0:
            for j in range(row+1,n)       :
                if M[row][j]!=0:
                    col=j
                    
        for i in range(row+1,n):
            if M[row][col]!=0:
                k.append(-1*M[i][col]/M[row][col])
            
        p=0
        for j in range(row+1,n):
            if len(k)!=0:
                rowOperationRow(M, j, row,k[p])
                p=p+1
            
def findSol(A,b,x,P):
    n=len(b)
    RANK_P=rank(P)
    RANK_A=rank(A)
    if RANK_A == n:
        A_inv=getInverse(A)
        print("Inverted A")
        printArr(A_inv)
        sol=multiplyMatrices(A_inv, b)
        print("Unique solution")
        for i in range(len(sol)):
            x[i]=sol[i]
        for i in range(len(x)):
            print("x",(i+1),"=","{:.3f}".format(x[i]),sep='')
    elif RANK_A <= n:
        pivoting(P)
        A=deepcopy(P)
        b=[i.pop(len(i)-1) for i in A]
        k=0
        temp=cleaningZeros(A,x,b)
        temp_inv=getInverse(temp)
        sol=multiplyMatrices(temp_inv, b)
        for i in range(len(sol)):
            x[i]=sol[i]
        print("Arbitrary Variables:",end='')
        for i in range(len(x)):
             if x[i]==0:
                 print("x",i+1,"=",x[i],sep='',end=' ')
        print()
        print("Arbitrary Solution")
        for i in range(len(x)):
            print("x",(i+1),"=","{:.3f}".format(x[i]),sep='')
        
    else:
        print("Inconsistent problem")
        return
    
def getInverse(M):
    if len(M)==1:
        CT=[]
        CT.append(1/M[0][0])
        return CT
    C=getCofactor(M)
    CT=getTranspose(C)
    multiplyMatrix(CT, 1/getDeterminant(M))
    return CT
      
def cleaningZeros(A,x,b):
    zeros=[]
    for i in range(len(A)):
        count=0
        for j in range(len(A[i])):
            if A[i][j]==0:
                count+=1
        if count == len(A[i]):
            zeros.append(i)
            if b[i]!=0:
                print("Inconsistent problem")
                return
    zeros.reverse()
    for i in range(len(zeros)):
        A=deletingCol(zeros[i], A)
        A=deletingRow(zeros[i], A)
        b.pop(zeros[i])   
    return A

def getDeterminant(A):
    determinant=0
    if len(A)==1:
        return A[0][0]
    if len(A)==2:
        determinant=(A[0][0]*A[1][1]-A[0][1]*A[1][0])
        return determinant
    temp=deepcopy(A)
    for i in range(len(A)):
        x=A[0][i]
        temp=deletingCol(i,A)
        temp=deletingRow(0,temp)
        determinant=determinant + x*((-1)**i)*getDeterminant(temp)
    return determinant

def getCofactor(M):
    C=deepcopy(M)           
    for i in range(len(M)):
        for j in range(len(M[i])):
            temp=deletingCol(j, M)
            temp=deletingRow(i,temp)
            C[i][j]=getDeterminant(temp)*((-1)**(i+j))
    return C        
   
def deletingCol(colNumber,M):
    temp=deepcopy(M)
    [i.pop(colNumber) for i in temp]
    return temp

def deletingRow(rowNumber,M):
    temp=[]
    for i in range(len(M)):
        if i!=rowNumber:
            temp.append(M[i])
    return temp     
      
def getTranspose(M):
    MT=deepcopy(M)
    for i in range(len(M)):
        for j in range(len(M[i])):
            MT[i][j]=M[j][i]
    return MT  

def getSolution(file):
    f=open(file)
    if (f.name.split(".")[1] == "txt"):
        print(file)
        n=f.readline()
        n=int(n)
        P=[]
        for line in f:
            line=line.split(' ')
            for i in range(0, len(line)): 
                line[i] = float(line[i]) 
            P.append(line)
        A=deepcopy(P)
        b=[i.pop(len(i)-1) for i in A]
        x=[0]*len(b)
        RANK_A=rank(A)
        RANK_P=rank(P)
        if RANK_A<RANK_P:
            print("Inconsistent problem")
        else:    
            findSol(A,b,x,P)
        print()
    
import os
entries=os.listdir(os.getcwd())
for i in range(len(entries)):
    getSolution(entries[i])




    
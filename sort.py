sort_list = [2,9,2,7,4,5,3]
str_list = ['123','124','56','90']

def isert_sort(A):
    print('bubble_sort run:')
    print('in list:', A)
    alen = len(A)
    for index in range(1,alen):
        k = index
        while k>0 and A[k-1] > A[k]:
            A[k-1], A[k] = A[k], A[k-1]
            k-=1
    print(A)
    print('bubble_sort done.')

def bubble_sort(A):
    #print('bubble_sort run:')
    #print('in list:', A)
    alen = len(A)
    for index in range(1,alen):
        for k in range(0, alen-index):
            if A[k] < A[k+1]:
                A[k], A[k+1] = A[k+1], A[k]
    return A
    #print(A)

def get_max(A):
    A = bubble_sort(A)    
    print(''.join(A))

if __name__ == "__main__":
    get_max(str_list)

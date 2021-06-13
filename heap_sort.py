# Create a function for heap sort 
#heapify
def heapify(arr,n,i):
    largest=i # largest value
    left=2*i+1 # left side
    right=2*i+2 # right side
    # if left child exists
    if left<n and arr[i]<arr[left]:
        largest=left
    # if right child exists
    if right<n and arr[largest]<arr[right]:
        largest=right
    # root
    if largest!=i:
        arr[i],arr[largest]=arr[largest],arr[i]
        heapify(arr,n,largest)
# Heap Sort
def heap_sort(arr):
    n=len(arr)
    # max heap
    for i in range(n,-1,-1):
        heapify(arr,n,i)
    for i in range(n-1,0,-1):
        arr[i],arr[0]=arr[0],arr[i]
        heapify(arr,i,0)
# In main, Create an user defined array & then print it
arr=list(map(int,input().split()))
heap_sort(arr)
print(arr)

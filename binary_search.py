# Create a function with 2 parameter
def binary_search(arr,key):
    # start & end initialization
    start=0
    end=len(arr)-1
    # check condition
    while start<=end:
        mid=start+(end-start)//2 # mid calculation
        if arr[mid]==key:  return mid # if element present in the middle of arr[]
        elif arr[mid]<key: start=mid+1 # if key is greater than mid
        else: end=mid-1 # else key is less than mid
    return "NOT FOUND" # key os not found in array
# In main, create user-defined array & key and then print it
arr=list(map(int,input().split()))
key=int(input())
print(binary_search(arr,key))

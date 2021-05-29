# Create a function with 2 parameter
def linear_search(arr,key):
    #start from the left most element of given arr[]
    for i in range(len(arr)):
        # one by one comapare with element key with each element of arr[]
        if arr[i]==key: return i # If key matches with any element, return index value
    return "NOT FOUND" # If key doesn't matches with any element, then return NOT FOUND
# In main, create user defined-array & key & then print
arr=list(map(int,input().split()))
key=int(input())
print(linear_search(arr,key))

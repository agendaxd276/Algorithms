# Create a function for insertion sort
def insertion_sort(arr):
    # Outer for loop traverse through 1 to len(arr)
    for i in range(1,len(arr)):
        # If condition is satisfied then swap it
        while arr[i-1]>arr[i] and i>0:
            arr[i],arr[i-1]=arr[i-1],arr[i] # swap
            i-=1 # continue comparison in between array elements
    return arr # return sorted array
# In main, Create a user-defined array & then print it
arr=list(map(int,input().split()))
print(insertion_sort(arr))

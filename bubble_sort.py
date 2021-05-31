# Create a function for bubble sort
def bubble_sort(arr):
    # set flag True or False
    sorted=False
    #check condition
    while not sorted:
        sorted=True
        # sort index 0 to index(n-1), so last element of array will automatically sorted
        for i in range(0,len(arr)-1):
            # Check condition for ascending or descending order
            if arr[i]<arr[i+1]:
                sorted=False
                arr[i],arr[i+1]=arr[i+1],arr[i] #swap elements
    return arr # return sorted array
# In main, Create a user-defined array & print it
arr=list(map(int,input().split()))
print(bubble_sort(arr))

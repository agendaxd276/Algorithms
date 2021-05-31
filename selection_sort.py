# Create a function for selection sort
def selection_sort(arr):
    # traverse through all elements in array
    for i in range(len(arr)):
        # Initially, assume that the first element of unsorted part in array is minimum
        min=i
        # Right unsorted part of outer for loop in array
        for j in range(i+1,len(arr)):
            # Check condition for ascending or descending order
            if arr[j]>arr[min]:
                min=j # update the position of minimum element if a smaller element is found
        if min!=i:
            arr[min],arr[i]=arr[i],arr[min] # swap the minimum element with the first element of the array (unsorted)
    return arr # return sorted array
# In main, Create an user defined array & then print it
arr=list(map(int,input().split()))
print(selection_sort(arr))

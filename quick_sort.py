# Create a function for quick sort
def quick_sort(arr):
    # Check Condition
    if len(arr)<=1:
        return arr
    else:
        pivot=arr.pop()
    # Create 2 lists
    greater_items=[]
    lower_items=[]
    # traverse through all items in array
    for item in arr:
        # Check condition for greater & lower items
        if item<pivot:
            lower_items.append(item)
        else:
            greater_items.append(item)
    # print like lower_items + pivot + greater items
    return quick_sort(lower_items)+[pivot]+quick_sort(greater_items)
# In main, Create a user-defined array & then print it
arr=list(map(int,input().split()))
print(quick_sort(arr))

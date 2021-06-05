# Create a function for merge sort
def merge_sort(arr):
    if len(arr)>1:
        # calculation
        mid=len(arr)//2
        # left: before mid
        left=arr[:mid]
        # right: after mid
        right=arr[mid:]
        # Recursive call on each half part
        merge_sort(left)
        merge_sort(right)
        # two iterators for traversing the two halves
        i=0
        j=0
        # Iterator for the main list
        k=0
        while i<len(left) and j<len(right):
            if left[i]<=right[j]:
                # the value from left half has been used
                arr[k]=left[i]
                # move the iterator forward
                i+=1
            else:
                arr[k]=right[j]
                j+=1
            # Move to the next slots
            k+=1
        # For all the remaining values in the array
        while i<len(left):
            arr[k]=left[i]
            i+=1
            k+=1
        while j<len(right):
            arr[k]=right[j]
            j+=1
            k+=1
# In main, Create a user-defined array & decleare & print it
arr=list(map(int,input().split()))
merge_sort(arr)
print(arr)

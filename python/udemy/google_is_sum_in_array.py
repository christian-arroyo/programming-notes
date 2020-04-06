def is_sum_in_array(array, sum):
    i = 0
    while(i < len(array)):
        j = 0
        while(j < len(array)):
            if array[i] + array[j] == sum:
                return True
            j += 1
        i += 1
    return False

array = [1, 3, 3, 9]
sum = 6
print(is_sum_in_array(array, sum))

# for(i=0; i < array.length(); i++){
#     for(j=i+1; j < arrlay.length(), j++){
#         if(array[i] + array[j] == sum){
#             return true
#         }
#     }
# }
# return false

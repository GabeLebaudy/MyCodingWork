nums1 = [1, 2]
nums2 = [3, 4]

i, j, mergedArr = 0, 0, []
while i < len(nums1) and j < len(nums2):
    if nums1[i] < nums2[j]:
        mergedArr.append(nums1[i])
        i += 1
    else:
        mergedArr.append(nums2[j])
        j += 1

while i < len(nums1):
    mergedArr.append(nums1[i])
    i += 1

while j < len(nums2):
    mergedArr.append(nums2[j])
    j += 1

medianInd = len(mergedArr) // 2
if len(mergedArr) % 2 == 0:
    median = (mergedArr[medianInd - 1] + mergedArr[medianInd]) / 2
else:
    median = mergedArr[medianInd]
    
print(median)
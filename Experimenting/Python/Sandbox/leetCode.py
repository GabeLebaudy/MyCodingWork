def longestPalindrome(s):
    """
    :type s: str
    :rtype: str
    """
    if checkPalindrome(s):
        return s
    
    best = ''
    for i in range(0, len(s)):
        for j in range(1, len(s)):
            if len(best) > len(s) - i:
                return best
            
            if j < len(s) - 1:
                segment = s[i:j + 1]
                isPalindrome = checkPalindrome(segment)
            else:
                segment = s[i:]
                isPalindrome = checkPalindrome(segment)

            if isPalindrome:
                if len(segment) > len(best):
                    best = segment
                
    return best

def checkPalindrome(arr):
    if len(arr) <= 1:
        return True

    startInd, exitInd = 0, len(arr) - 1
    while startInd != exitInd and startInd < exitInd:
        if arr[startInd] != arr[exitInd]:
            return False
        startInd += 1
        exitInd -= 1

    return True 

print(longestPalindrome("babad"))
print(longestPalindrome("wsgdzojcrxtfqcfkhhcuxxnbwtxzkkeunmpdsqfvgfjhusholnwrhmzexhfqppatkexuzdllrbaxygmovqwfvmmbvuuctcwxhrmepxmnxlxdkyzfsqypuroxdczuilbjypnirljxfgpuhhgusflhalorkcvqfknnkqyprxlwmakqszsdqnfovptsgbppvejvukbxaybccxzeqcjhmnexlaafmycwopxntuisxcitxdbarsicvwrvjmxsapmhbbnuivzhkgcrshokkioagwidhmfzjwwywastecjsolxmhfnmgommkoimiwlgwxxdsxhuwwjhpxxgmeuzhdzmuqhmhnfwwokgvwsznfcoxbferdonrexzanpymxtfojodcfydedlxmxeffhwjeegqnagoqlwwdctbqnuxngrgovrjesrkjrfjawknbrsfywljscfvnjhczhyeoyzrtbkvvfvofykkwoiclgxyaddhpdoztdhcbauaagjmfzkkdqexkczfsztckdlujgqzjyuittnudpldjvsbwbzcsazjpxrwfafievenvuetzcxynnmskoytgznvqdlkhaowjtetveahpjguiowkiuvikwewmgxhgfjuzkgrkqhmxxavbriftadtogmhlatczusxkktcsyrnwjbeshifzbykqibghmmvecwwtwdcscikyzyiqlgwzycptlxiwfaigyhrlgtjocvajcnqyenxrnjgogeqtvkxllxpuoxargzgcsfwavwbnktchwjebvwwhfghqkcjhuhuqwcdsixrkfjxuzvhjxlyoxswdlwfytgbtqbeimzzogzrlovcdpseoafuxfmrhdswwictsctawjanvoafvzqanvhaohgndbsxlzuymvfflyswnkvpsvqezekeidadatsymbvgwobdrixisknqpehddjrsntkqpsfxictqbnedjmsveurvrtvpvzbengdijkfcogpcrvwyf"))
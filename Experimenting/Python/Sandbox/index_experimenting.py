def caesarCipher(s, k):
    new_str = ""
    for char in s:
        new_char = char
        ord_num = ord(char)
        if 65 <= ord_num <= 90:
            ord_num += k
            if ord_num > 90:
                ord_num -= 26
                
            new_char = chr(ord_num)
            
        if 97 <= ord_num <= 122:
            ord_num += k
            if ord_num > 122:
                ord_num -= 26
            
            new_char = chr(ord_num)
            
        new_str += new_char
    return new_str


print(caesarCipher("www.abc.xy", 87))

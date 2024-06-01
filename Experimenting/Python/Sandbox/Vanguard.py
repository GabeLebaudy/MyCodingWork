#This file will be for testing the vanguard coding assesment 

#Imports


def isPangram(pangram):
    final_str = ""
    for string in pangram:
        cache = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        
        for letter in string:
            if 97 <= ord(letter) <= 122:
                cache[ord(letter) - 97] += 1
        
        print(cache)
        did_add = False
        for key in cache:
            if key == 0:
                print("Yo!")
                final_str += "0"
                did_add = True
                break
        
        if not did_add:
            final_str += "1"
    
    return final_str

#Main
if __name__ == "__main__":
    final_str = isPangram(["cfchcfcvpalpqxenhbytcwazpxtthjumliiobcznbefnofyjfsrwfecxcbmoafes tnulqkvx"])
    print(final_str)
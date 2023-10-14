#This file will be used to investigate Hash Maps using linear probing

class HashMap:  
    #Constructor
    def __init__(self):
        self.MAX = 10 # I am keeping size very low to demonstrate linear probing easily but usually the size should be high
        self.arr = [None for i in range(self.MAX)]
    
    #Generates hash key using the conversion from character to integer value in ASCII, and the getting the remainder.
    def get_hash(self, key):
        hash = 0
        for char in key:
            hash += ord(char)
        return hash % self.MAX
    
    #Returns the value of a key
    def __getitem__(self, key):
        #Passes the key into the hash function to find the hash value
        h = self.get_hash(key)

        #If the slot is empty, it just returns nothing
        if self.arr[h] is None:
            return
        
        #Gets a list of values that the value could be in. The values are generated in the same way that the item would be placed in should the bucket be full. 
        prob_range = self.get_prob_range(h)
        for prob_index in prob_range:
            element = self.arr[prob_index]

            #Since the item would be placed in the first empty bucket, if we encounter an empty bucket, we can confirm that the item is not there.
            if element is None:
                return
            
            #The element was found
            if element[0] == key:
                return element[1]
    
    #Inserts a new value into the hashmap, or modifies a previous value.
    def __setitem__(self, key, val):
        #Gets the hash key
        h = self.get_hash(key)

        #The bucket is empty, so we can just fill it
        if self.arr[h] is None:
            self.arr[h] = (key,val)
        
        #The bucket isn't empty
        else:
            #Finds a new hash key
            new_h = self.find_slot(key, h)
            #Assigns the slot in the array to a tuple with key and val
            self.arr[new_h] = (key,val)
        
        #Prints for effect (Not necessary)
        print(self.arr)
    
    #Gets two lists, then combines them. The first list is indexes from 1 to the length of the array, the second is from 0 to the index.
    def get_prob_range(self, index):
        return [*range(index, len(self.arr))] + [*range(0,index)]
    
    #Called in case of a bucket being full
    def find_slot(self, key, index):
        #Gets the range of buckets to check in specific order
        prob_range = self.get_prob_range(index)
        for prob_index in prob_range:
            #If the bucket at the new index is empty return that index
            if self.arr[prob_index] is None:
                return prob_index
            
            #If it found a bucket with the same key, it returns that index
            if self.arr[prob_index][0] == key:
                return prob_index
            
        #If it gets here, it has exhausted all options and the map is full.
        raise Exception("Hashmap full")
    
    #Removes item from hash map
    def __delitem__(self, key):
        #Gets the hash key
        h = self.get_hash(key)

        #Finds the probe range using the hash key
        prob_range = self.get_prob_range(h)
        for prob_index in prob_range:
            #Bucket is empty, so the item wasn't found
            if self.arr[prob_index] is None:
                return # item not found so return. You can also throw exception
            #Sets the bucket to None if the key is found
            if self.arr[prob_index][0] == key:
                self.arr[prob_index]=None
        #Prints new values for effect
        print(self.arr)
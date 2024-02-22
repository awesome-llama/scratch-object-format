
USE_VALUE_ONLY_OBJECTS = False

# V=value, P=pointer, A=array, D=dict, AV=array of values, DV=dict of values

class IterateAddresses:
    """Count from a start value for a given number of times and step size"""

    def __init__(self, repeat, start=0, step=1):
        self.i = start - step
        self.i_max = start + repeat*step
        self.step = step

    def __iter__(self):
        return self

    def __next__(self):
        self.i += self.step
        if self.i < self.i_max:
            return self.i
        else:
            raise StopIteration


def encode(obj, as_string=True):

    def contains_values_only(obj):
        """Determine whether the object has anything nested"""

        if isinstance(obj, dict):
            for e in obj.values():
                if isinstance(e, list) or isinstance(e, dict):
                    return False
        else:
            for e in obj:
                if isinstance(e, list) or isinstance(e, dict):
                    return False
        return True


    def add_object(output: list, obj):
        """Recursive function to add objects to the output list"""
        address = len(output) # the index of the start of the object in the list
        
        if isinstance(obj, list):
            
            if USE_VALUE_ONLY_OBJECTS and contains_values_only(obj):
                output.extend(['AV', len(obj)] + obj) # concatenate value list
            
            else:
                output.extend(['A', len(obj)] + [None]*(len(obj)*2))
                
                for i, e in enumerate(obj):
                    i = address+2 + i*2
                    nested_obj = add_object(output, e)
                    output[i] = nested_obj[0]
                    output[i+1] = nested_obj[1]
                
            return ['P', address+1]
        
        elif isinstance(obj, dict):
            if USE_VALUE_ONLY_OBJECTS and contains_values_only(obj):
                output.extend(['DV', len(obj)] + [None]*(len(obj)*2))

                for i, kv in enumerate(obj.items()):
                    i = address+2 + i*2
                    output[i] = kv[0]
                    output[i+1] = kv[1]
            else:
                output.extend(['D', len(obj)] + [None]*(len(obj)*3))
                for i, kv in enumerate(obj.items()):
                    i = address+2 + i*3
                    output[i] = kv[0] # key
                    nested_obj = add_object(output, kv[1])
                    output[i+1] = nested_obj[0] # object type
                    output[i+2] = nested_obj[1] # value
            
            return ['P', address+1] # add 1 for scratch 1-indexed lists

        else:
            return ['V', obj] # add value

    output = [] 
    root = add_object(output, obj)
    
    if root[0] != 'P':
        # not a pointer, store it
        output = root

    if as_string:
        return [str(x) for x in output] # convert to a string (for scratch)
    else:
        return output



def decode(obj):
    """Decode the hierarchical object format, output a nested structure."""

    def get_object(obj: list, address=1):
        """Recursive function. Address should be 1-indexed."""

        adr = int(address) - 1 # adr is 0-indexed

        match obj[adr]:
            case 'V':
                return obj[adr+1]
            
            case 'P':
                return get_object(obj, int(obj[adr+1]))
            
            case 'A':
                output = []
                for i in IterateAddresses(int(obj[adr+1]), adr+2, 2):
                    output.append(get_object(obj, i+1))
                return output
            
            case 'AV':
                output = []
                for i in IterateAddresses(int(obj[adr+1]), adr+2, 1):
                    output.append(obj[i])
                return output

            case 'D':
                output = {}
                for i in IterateAddresses(int(obj[adr+1]), adr+2, 3):
                    output[obj[i]] = get_object(obj, i+2)
                return output

            case 'DV':
                output = {}
                for i in IterateAddresses(int(obj[adr+1]), adr+2, 2):
                    output[obj[i]] = obj[i+1]
                return output

            case _:
                raise Exception(f'object type unknown: {obj[adr]}')
            
    return get_object(obj, 1)


if __name__ == '__main__':
    def test(obj):
        encoded = encode(obj)
        print('source:', obj)
        print('encode:', encoded)
        print('decode:', decode(encoded))
        print('')
    
    test(["alfa","bravo","charlie","delta","echo"])
    test({"a":"alfa","b":"bravo","c":"charlie","d":"delta","e":"echo"})
    test([])
    test([{"a":"alfa"}, 123])
    test({"a":[4,5,6],"b":123,"c":91})
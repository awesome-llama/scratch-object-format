
USE_VALUE_ONLY_OBJECTS = True

# V=value, P=pointer, A=array, D=dict, AV=array of values, DV=dict of values

class IterateAddresses:
    """Iterator for addresses"""

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
    
    output = [1] # start with an item to replace later

    def contains_values_only(obj):
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

        if isinstance(obj, list):
            # determine whether the array has anything nested

            if USE_VALUE_ONLY_OBJECTS and contains_values_only(obj):
                contents = ['AV', len(obj)]
                contents.extend(obj)
            else:
                contents = ['A', len(obj)]
                for e in obj:
                    contents.extend(add_object(output, e))
                
            address = len(output) + 1
            output.extend(contents)
            return ['P', address]
        
        elif isinstance(obj, dict):
            if USE_VALUE_ONLY_OBJECTS and contains_values_only(obj):
                contents = ['DV', len(obj)]
                for k,v in obj.items():
                    contents.append(k)
                    contents.append(v)
            else:
                contents = ['D', len(obj)]
                for k,v in obj.items():
                    contents.append(k)
                    contents.extend(add_object(output, v))
            
            address = len(output) + 1
            output.extend(contents)
            return ['P', address]

        else:
            return ['V', obj]


    root = add_object(output, obj)
    if root[0] == 'P':
        output[0] = root[1]
    else:
        # value
        output[0] = len(output) + 1
        output.extend(root)

    if as_string:
        return [str(x) for x in output]
    else:
        return output



def decode(obj):

    def add_object(obj: list, address):
        """Recursive function"""

        address = int(address)

        match obj[address]:
            case 'V':
                return obj[address+1]
            
            case 'P':
                return add_object(obj, int(obj[address+1]) - 1)
            
            case 'A':
                output = []
                for i in IterateAddresses(int(obj[address+1]), address+2, 2):
                    output.append(add_object(obj, i))
                return output
            
            case 'AV':
                output = []
                for i in IterateAddresses(int(obj[address+1]), address+2, 1):
                    output.append(obj[i])
                return output

            case 'D':
                output = {}
                for i in IterateAddresses(int(obj[address+1]), address+2, 3):
                    output[obj[i]] = add_object(obj, i+1)
                return output

            case 'DV':
                output = {}
                for i in IterateAddresses(int(obj[address+1]), address+2, 2):
                    output[obj[i]] = obj[i+1]
                return output

            case _:
                raise Exception('data type unknown')
            
    return add_object(obj, int(obj[0])-1)
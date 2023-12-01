import helper.py

#
# part 1
#
get_task(1)

input = get_input(1)
numchars = [ re.findall('\d',i) for i in input ]
numbers = [ int( n[0] + n[-1] ) for n in numchars ]
answer = sum(numbers)

submit(1, 1, answer)


#
# part 2
#
get_task(1)


textual_numbers = {'one': '1', 'two': '2', 'three': '3', 'four': '4', 'five': '5', 'six': '6', 'seven': '7', 'eight': '8', 'nine': '9'}

def get_first_number(str):
    if str[0] >= '0' and str[0] <= '9':
        return str[0]
    
    for k,v in textual_numbers.items():
        if str.startswith(k):
            return(v)
    
    if len(str) == 1:
        raise Exception('no numbers found')
    
    return get_first_number(str[1:])

def get_last_number(str):
    if str[-1] >= '0' and str[-1] <= '9':
        return str[-1]
    
    for k,v in textual_numbers.items():
        if str.endswith(k):
            return(v)
    
    if len(str) == 1:
        raise Exception('no numbers found')
    
    return get_last_number(str[:-1])


input = get_input(1)
numbers = [ int( get_first_number(i) + get_last_number(i) ) for i in input ]
answer = sum(numbers)

submit(1, 2, answer)
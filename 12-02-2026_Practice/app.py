# def find_patient(search_name):
#     if search_name.strip().lower() == 'john smit':
#         return "Patient: John Smit"
#     else:
#         return None
#
# user_input = input("Enter the name:")
#
# result = find_patient(user_input)
#
# if result:
#     print(f"Match found: {result}")
# else:
#     print(f"Match not found")
#



#Sum
# def sum_of_two_numbers(a,b):
#     return a+b
# num1 = int(input("Enter first number: "))
# num2 = int(input("Enter second number: "))
#
# s = sum_of_two_numbers(num1,num2)
# print(f"The sum of two numbers : {s}")



#Find Weight
# def find_weight(w,u):
#        if u.upper() == "K":
#               return w/0.45
#        elif u.upper() == "L":
#               return w*0.45
#        return 0
# weight = int(input("Enter Weight :"))
# unit = input("(K)g or (L)bs:")
#
# f = find_weight(weight,unit)

#print("Converted weight:",round(f,2))



#Find ages

def find_oldest_age(a,b,c):
    if a>b and a>c:
        return a
    elif b>c and b>a:
        return b
    elif c>a and c>b:
        return c
    else:
        print("Invalid Input")

f = find_oldest_age(1,5,3)
print(f)










































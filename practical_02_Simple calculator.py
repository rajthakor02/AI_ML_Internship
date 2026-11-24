num1 = int(input("Enter the first number: "))
num2 = int(input("Enter the second number: "))

print("Addition:",num1 + num2)
print("Subtraction:",num1 - num2)
print("Multiplication:",num1 * num2)

if num2 != 0:
    print("Division:",num1/num2)
else:
    print("Division is not possible because of the second number is zero!")
    
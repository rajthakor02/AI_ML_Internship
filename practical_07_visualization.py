import matplotlib.pyplot as plt
names = ["Asha", "Rahul", "Meena", "Dev"]
marks = [78, 85, 92, 65]
plt.bar(names, marks)
plt.title("Student Marks")
plt.xlabel("Student")
plt.ylabel("Marks")
plt.ylim(0, 100)

plt.show()
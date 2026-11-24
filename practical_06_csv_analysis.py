import pandas as pd 
data = {
 "Name": ["raj", "dipak", "dishant", "shaniya"],
 "Marks": [78, 85, 92, 65]
}
df = pd.DataFrame(data)

df.to_csv("students.csv",index=False)

students = pd.read_csv("Students.csv")

average = students["Marks"].mean()

print("Students recorders:")
print(students)
print("Class average:",average)
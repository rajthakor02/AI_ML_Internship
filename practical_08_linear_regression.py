from sklearn.linear_model import LinearRegression
import pandas as pd

data = {
    "hours": [1,2,3,4,5,6,7,8],
    "score": [35, 40, 50, 55, 65, 70, 80, 85]
}

df = pd.DataFrame(data)

x = df[["hours"]]
y = df["score"]

model = LinearRegression()

model.fit(x,y)

new_student = pd.DataFrame({"hours": [4.5]})
predicted_score = model.predict(new_student)

print("Predicted score:",round(predicted_score[0], 2))

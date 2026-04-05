import gradio as gr
import pickle
import pandas as pd

# মডেল লোড করা
with open('ipl_model.pkl', 'rb') as file:
    data = pickle.load(file)

model = data["model"]
encoders = data["encoders"]

def predict_winner(team1, team2, toss_winner, toss_decision, venue, season):
    # ইনপুট ডেটা প্রসেসিং
    input_data = pd.DataFrame([[
        encoders['team1'].transform([team1])[0],
        encoders['team2'].transform([team2])[0],
        encoders['toss_winner'].transform([toss_winner])[0],
        encoders['toss_decision'].transform([toss_decision])[0],
        encoders['venue'].transform([venue])[0],
        encoders['season'].transform([season])[0],
        0.5, 0.5, 0.5 # Default Form values
    ]], columns=['team1', 'team2', 'toss_winner', 'toss_decision', 'venue', 'season', 'team1_form', 'team2_form', 'head_to_head'])

    prediction = model.predict(input_data)
    winner = encoders['winner'].inverse_transform(prediction)[0]
    return f"The predicted winner is: {winner}"

# Gradio ইন্টারফেস তৈরি
interface = gr.Interface(
    fn=predict_winner,
    inputs=[
        gr.Dropdown(list(encoders['team1'].classes_), label="Select Team 1"),
        gr.Dropdown(list(encoders['team2'].classes_), label="Select Team 2"),
        gr.Dropdown(list(encoders['toss_winner'].classes_), label="Toss Winner"),
        gr.Dropdown(list(encoders['toss_decision'].classes_), label="Toss Decision"),
        gr.Dropdown(list(encoders['venue'].classes_), label="Venue"),
        gr.Dropdown(list(encoders['season'].classes_), label="Season")
    ],
    outputs="text",
    title="IPL Match Winner Predictor",
    description="Enter match details to predict the winner using Machine Learning."
)

if __name__ == "__main__":
    interface.launch()

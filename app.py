import gradio as gr
import pickle
import pandas as pd

# ডেমো ফাংশন (এখন শুধু টেস্ট)
def predict(team1, team2, toss_winner, venue):
    # বাস্তবে এখানে মডেল বসবে
    return f"🏆 {team1} জিতবে! (ডেমো)"

# Gradio UI
demo = gr.Interface(
    fn=predict,
    inputs=[
        gr.Dropdown(["CSK", "MI", "RCB", "KKR", "SRH", "PBKS"], label="Team 1"),
        gr.Dropdown(["CSK", "MI", "RCB", "KKR", "SRH", "PBKS"], label="Team 2"),
        gr.Dropdown(["CSK", "MI", "RCB", "KKR", "SRH", "PBKS"], label="Toss Winner"),
        gr.Dropdown(["Wankhede", "Eden Gardens", "Chinnaswamy", "Narendra Modi"], label="Venue")
    ],
    outputs="text",
    title="🏏 IPL Winner Predictor",
    description="দুই দলের নাম, টস জেতা দল ও ভেন্যু দিন → বলে দেবে কে জিতবে!"
)

if __name__ == "__main__":
    demo.launch()
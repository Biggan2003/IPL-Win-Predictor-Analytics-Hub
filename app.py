import gradio as gr

def predict_winner(team1, team2, toss_winner, venue, season):
    if toss_winner == team1:
        return f"🏆 {team1} জিতবে!"
    else:
        return f"🏆 {team2} জিতবে!"

demo = gr.Interface(
    fn=predict_winner,
    inputs=[
        gr.Dropdown(["CSK", "MI", "RCB", "KKR"], label="Team 1"),
        gr.Dropdown(["CSK", "MI", "RCB", "KKR"], label="Team 2"),
        gr.Dropdown(["CSK", "MI", "RCB", "KKR"], label="Toss Winner"),
        gr.Dropdown(["Wankhede", "Eden Gardens"], label="Venue"),
        gr.Dropdown(["2023/24", "2024/25"], label="Season")
    ],
    outputs="text"
)

demo.launch()

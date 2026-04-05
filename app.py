import gradio as gr
import joblib
import pandas as pd
import numpy as np

# ১. মডেল এবং এনকোডার লোড করা
try:
    data = joblib.load('ipl_model.joblib')
    model = data["model"]
    encoders = data["encoders"]
    all_teams = sorted(list(encoders['team1'].classes_))
    all_venues = sorted(list(encoders['venue'].classes_))
    all_seasons = sorted(list(encoders['season'].classes_))
    all_decisions = sorted(list(encoders['toss_decision'].classes_))
except Exception as e:
    print(f"Error loading model: {e}")

def predict_winner(team1, team2, toss_winner, toss_decision, venue, season):
    try:
        # ১. ইনপুট এনসিওর করা (যাতে কোনোভাবেই None না যায়)
        t1 = str(team1) if (team1 and str(team1) != "None") else all_teams[0]
        t2 = str(team2) if (team2 and str(team2) != "None") else all_teams[1]
        
        # টস উইনার হ্যান্ডলিং
        if not toss_winner or str(toss_winner) == "None":
            tw = t1
        else:
            tw = str(toss_winner)
            
        td = str(toss_decision) if toss_decision else "bat"
        vn = str(venue) if venue else all_venues[0]
        
        # সিজন হ্যান্ডলিং
        current_s = str(season) if season else "2024"
        ss = "2024" if current_s in ["2025", "2026"] else current_s

        # ২. ইনপুট ডাটা এনকোড করা
        input_dict = {
            'team1': encoders['team1'].transform([t1])[0],
            'team2': encoders['team2'].transform([t2])[0],
            'toss_winner': encoders['toss_winner'].transform([tw])[0],
            'toss_decision': encoders['toss_decision'].transform([td])[0],
            'venue': encoders['venue'].transform([vn])[0],
            'season': encoders['season'].transform([ss])[0]
        }
        
        cols = ['team1', 'team2', 'toss_winner', 'toss_decision', 'venue', 'season']
        input_df = pd.DataFrame([input_dict])[cols]

        # ৩. প্রোবাবিলিটি লজিক (The Final Override)
        # আমরা সরাসরি মডেলের প্রসেস করা ক্লাসগুলো চেক করব
        probs = model.predict_proba(input_df)[0]
        classes = list(encoders['winner'].classes_)
        
        # বর্তমান ম্যাচে থাকা ২ টিমের ইনডেক্স খুঁজে বের করা
        # যদি টিমগুলো এনকোডারে না থাকে তবে এরর হ্যান্ডেল করবে
        try:
            idx1 = classes.index(t1)
            idx2 = classes.index(t2)
        except ValueError:
            # যদি কোনো কারণে নাম না মেলে, তবে সরাসরি টস উইনারকে বিজয়ী করে দাও
            return f"🏆 Predicted Winner: {tw}"

        # শুধুমাত্র সিলেক্ট করা ২ টিমের মধ্যে কার প্রোবাবিলিটি বেশি?
        if probs[idx1] >= probs[idx2]:
            final_winner = t1
        else:
            final_winner = t2
        
        return f"🏆 Predicted Winner: {final_winner}"

    except Exception as e:
        print(f"DEBUG ERROR: {e}")
        # যদি সব লজিক ফেইল করে, তবে লজিক্যালি টস উইনারকেই বিজয়ী দেখাও
        return f"🏆 Predicted Winner: {team1 if team1 else 'Team 1'}"

# ৩. স্মার্ট টস উইনার লজিক
def update_toss_choices(t1, t2):
    choices = [t1, t2] if t1 and t2 else all_teams[:2]
    return gr.Dropdown(choices=choices, value=choices[0])

# ৪. ডিজাইন এবং ইউআই (অপরিবর্তিত)
custom_css = """
body { background-color: #0b0e14; }
.gradio-container { background-color: #0b0e14 !important; border: none !important; }
.main-box { background: #161b22; border-radius: 15px; padding: 20px; border: 1px solid #30363d; }
h1 { color: #f0f6fc !important; text-align: center; font-size: 2.5em; text-shadow: 2px 2px #1d3557; }
.link-text { text-align: center; margin-bottom: 20px; }
.predict-btn { 
    background: linear-gradient(135deg, #1d4ed8 0%, #1e40af 100%) !important; 
    color: white !important; font-weight: bold !important; border-radius: 10px !important; border: none !important;
}
label { color: #8b949e !important; font-weight: 600 !important; }
footer { display: none !important; }
"""

js_confetti = "function() { confetti({ particleCount: 150, spread: 70, origin: { y: 0.6 } }); }"

with gr.Blocks(css=custom_css, head='<script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.5.1/dist/confetti.browser.min.js"></script>') as demo:
    gr.HTML(f"""<h1>🏏 IPL Winner Predictor Pro</h1><div class="link-text"><a href="https://www.linkedin.com/in/g-m-biggan-371956305/" target="_blank" style="color: #58a6ff; font-weight: bold; text-decoration: none;">Developed by G.M. Biggan 🚀</a></div>""")
    
    with gr.Column(elem_classes="main-box"):
        with gr.Row():
            team1_input = gr.Dropdown(all_teams, label="🏠 Home Team", value="Chennai Super Kings")
            team2_input = gr.Dropdown(all_teams, label="✈️ Away Team", value="Punjab Kings")
        with gr.Row():
            venue_input = gr.Dropdown(all_venues, label="🏟️ Stadium", value=all_venues[0])
            season_input = gr.Dropdown(all_seasons + ["2025", "2026"], label="📅 Season", value="2026")
        with gr.Row():
            toss_winner_input = gr.Dropdown(choices=["Chennai Super Kings", "Punjab Kings"], label="🪙 Toss Winner", value="Chennai Super Kings")
            toss_decision_input = gr.Radio(all_decisions, label="🏏 Toss Decision", value=all_decisions[0])

    predict_btn = gr.Button("⚡ Predict Winner & Celebrate", elem_classes="predict-btn")
    result_output = gr.Textbox(label="Prediction Result", interactive=False)

    team1_input.change(update_toss_choices, inputs=[team1_input, team2_input], outputs=toss_winner_input)
    team2_input.change(update_toss_choices, inputs=[team1_input, team2_input], outputs=toss_winner_input)

    predict_btn.click(predict_winner, inputs=[team1_input, team2_input, toss_winner_input, toss_decision_input, venue_input, season_input], outputs=result_output, js=js_confetti)

if __name__ == "__main__":
    demo.launch()

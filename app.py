import gradio as gr
import joblib
import pandas as pd

# মডেল লোড
model = joblib.load('ipl_model.pkl')
encoders = joblib.load('label_encoders.pkl')

def predict_winner(team1, team2, toss_winner, venue, season):
    input_data = pd.DataFrame([[team1, team2, toss_winner, venue, season]], 
                              columns=['team1', 'team2', 'toss_winner', 'venue', 'season'])
    
    for col in ['team1', 'team2', 'toss_winner', 'venue', 'season']:
        input_data[col] = encoders[col].transform(input_data[col].astype(str))
    
    prediction = model.predict(input_data)[0]
    winner = encoders['winner'].inverse_transform([prediction])[0]
    
    return f"🏆 বিজয়ী দল: {winner}"

demo = gr.Interface(
    fn=predict_winner,
    inputs=[
        gr.Dropdown(['CSK', 'MI', 'RCB', 'KKR', 'SRH', 'PBKS', 'GT', 'LSG'], label="Team 1"),
        gr.Dropdown(['CSK', 'MI', 'RCB', 'KKR', 'SRH', 'PBKS', 'GT', 'LSG'], label="Team 2"),
        gr.Dropdown(['CSK', 'MI', 'RCB', 'KKR', 'SRH', 'PBKS', 'GT', 'LSG'], label="Toss Winner"),
        gr.Dropdown(['Wankhede', 'Eden Gardens', 'Chinnaswamy', 'Narendra Modi', 'Chepauk'], label="Venue"),
        gr.Dropdown(['2007/08', '2008/09', '2009/10', '2010/11', '2011/12', '2012/13', '2013/14', '2014/15', '2015/16', '2016/17', '2017/18', '2018/19', '2019/20', '2020/21', '2021/22', '2022/23', '2023/24'], label="Season")
    ],
    outputs=gr.Textbox(label="Result"),
    title="🏏 IPL Winner Predictor"
)

demo.launch()

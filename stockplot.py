import plotly.graph_objects as go

def simple_plot(df):
    fig=go.Figure(data=go.Ohlc(x=df['time'],
                    open=df['o'],
                    high=df['h'],
                    low=df['l'],
                    close=df['c']))
    fig.update(layout_xaxis_rangeslider_visible=False)
    fig.show()
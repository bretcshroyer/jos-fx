import plotly.graph_objects as go

def simple_plot(df):
    fig=go.Figure(data=go.Ohlc(x=df['time'],
                    open=df['o'],
                    high=df['h'],
                    low=df['l'],
                    close=df['c']))
    fig.update(layout_xaxis_rangeslider_visible=False)
    fig.update_layout(
        xaxis=dict(
            showticklabels=False,
            showgrid=False,
            zeroline=False,
            showline=False
        ),
        yaxis=dict(
            showticklabels=False,
            showgrid=False,
            zeroline=False,
            showline=False
        ),
        showlegend=False,
        hovermode=False,
        xaxis_rangeslider_visible=False
    )

    fig.show()
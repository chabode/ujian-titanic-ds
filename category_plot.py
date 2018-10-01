import plotly.graph_objs as go 

def getPlot(jenis,xCategory,text):
    return [listGOFunc[jenis](
                x=dfTips[xCategory],
                y=dfTips['tip'],
                text=dfTips[text],
                opacity=0.7,
                name='Tip',
                legendgroup='Tip',
                marker=dict(color='blue')
            ),
            listGOFunc[jenis](
                x=dfTips[xCategory],
                y=dfTips['total_bill'],
                text=dfTips[text],
                opacity=0.7,
                name='Total Bill',
                legendgroup='TotalBill',
                marker=dict(color='orange')
            )
    ]
from ParallelCoordinates import ParallelCoordinates
import pandas as pd
import plotly.plotly as py
import os

py.sign_in('DemoAccount', '2qdyfjyr7o')

df = pd.read_csv('../data/iris.csv')


def test_ParallelCoordinates_plot():
    pc = ParallelCoordinates(df)
    pc.set_layout(plot_bgcolor='#E5E5E5',
            paper_bgcolor='#E5E5E5')
    pc.plot('species',
            labels=['Sepal length', 'Sepal width', 'Petal length', 'Petal width'],
            ranges=[[0,8],[0,8],[0,8],[0,8]])


def test_ParallelCoordinates_save():
    pc = ParallelCoordinates(df)
    pc.plot('species')
    pc.save(output_filename='../data/save_test.png')
    assert os.path.isfile('../data/save_test.png')
    os.remove('../data/save_test.png')

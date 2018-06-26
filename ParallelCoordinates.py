from plotly.offline import plot, iplot, init_notebook_mode
import plotly.graph_objs as go
import plotly.plotly as py
import pandas as pd
import sys


def is_kernel() -> bool:
    """
    Determine if I am in a IPython/Jupyter notebook environment
    """
    if 'IPython' not in sys.modules:
        # IPython hasn't been imported, definitely not
        return False
    from IPython import get_ipython
    # check for `kernel` attribute on the IPython instance
    return getattr(get_ipython(), 'kernel', None) is not None


class ParallelCoordinates:
    """
    Represents a parallel coordinates plot for the given pandas dataframe.
    """

    def __init__(self, df: pd):
        """
        :param df: Pandas dataframe to be plotted.
        """
        self.df = df
        self.data = None
        self._fig = None
        self.layout = go.Layout(
            plot_bgcolor='#FFF',
            paper_bgcolor='#FFF',
            showlegend=True
        )
        self.plotting_method = plot
        if is_kernel():
            init_notebook_mode(connected=True)
            self.plotting_method = iplot

    def set_layout(self, **kwargs):
        """
        Configure the plot layout
        :param kwargs: every available parameter for plotly.graph_objs.Layout (https://plot.ly/python/reference/#layout)
        :return:
        """
        self.layout.update(**kwargs)

    def plot(self, class_column, colorscale='RdBu', labels=None, ranges=None):
        """
        Build a parallel coordinates plot.
        :param class_column: Column of the pandas dataframe expected to be the "class", i.e, for every
        unique value on this column, one line color.
        :param colorscale: plotly colorscale (https://plot.ly/python/colorscales/).
        :param labels: Name of every dimension.
        :param ranges: Range to be plotted in every dimension.
        :return:
        """
        if labels is not None:
            if len(labels) != len(list(self.df)) - 1:
                raise ValueError("'labels' must be a list of length equal to the number of columns"
                                 " of the dataframe minus one.")
        else:
            labels = []
            for column in list(self.df):
                labels.append(column)

        if ranges is not None:
            if len(ranges) != len(list(self.df)) - 1:
                raise ValueError("'ranges' must be a list of length equal to the number of columns"
                                 " of the dataframe minus one.")
        else:
            ranges = []
            for column in list(self.df):
                ranges.append([min(self.df[column]), max(self.df[column])])

        dimensions = []
        for index, column in enumerate(list(self.df)):
            if not column == class_column:
                dimensions.append(dict(
                    range=ranges[index],
                    label=labels[index],
                    values=self.df[column]
                ))

        colormap = {k: i for i, k in enumerate(self.df[class_column].unique())}
        self.data = [
            go.Parcoords(
                line=dict(
                    color = list(map(lambda x: colormap[x], self.df[class_column])),
                    colorscale=colorscale,
                    showscale=True
                ),
                dimensions=dimensions
            )
        ]
        self._fig = go.Figure(data=self.data, layout=self.layout)
        return self.plotting_method(self._fig)

    def save(self, output_filename, image_height=600, image_width=600) -> None:
        """
        Saves the current plot into a file. PNG and JPEG formats supported.
        *Requires internet connection. Requires a plot.ly account and API key*
        :param output_filename: name of the image file with png or jpeg extension.
        For other extensions we require a Professional account on plot.ly.
        :param image_height: height of image in pixels.
        :param image_width: width of image in pixels.
        """
        py.image.save_as(self._fig, filename=output_filename, height=image_height, width=image_width)

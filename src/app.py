from dash import Dash, html, dcc, callback, Output, Input, dash_table
import dash_bootstrap_components as dbc

# ---------------------------------------------------------------------------- #
#               import graph containers and callbacks from files               #
# ---------------------------------------------------------------------------- #

from topic_graphs import (
    topic_container, get_topic_callbacks,
    bar_topic_container, get_topic_bar_callbacks,
    artist_bar_topic_container, get_artist_bar_topic_callbacks,
    topic_scatter_container, get_topic_scatter_callbacks,
    topic_md_1,
    genre_hist_topic_container, get_genre_hist_topic_callbacks
    )

from example_lyrics import (
    topic_max_md_1, topic_max_df_table
)

from frequency_graphs import (
    artist_freq_dist_container, get_artist_freq_dist_callbacks,
    genre_freq_dist_container, get_genre_freq_dist_callbacks,
    freq_md_1
)

from metadata_graphs import (
    genre_metadata_container, get_genre_metadata_callbacks,
    genre_hist_metadata_container, get_genre_hist_meta_callbacks,
    artist_metadata_container, get_artist_metadata_callbacks,
    bar_line_metadata_container, get_bar_line_metadata_callbacks,
    bar_line_metadata_topic_container, get_bar_line_metadata_topic_callbacks,
    meta_md_1
)

from static_graphs import (
    corr_container,
    topic_spine_container,
    genre_sentiment_spine_container,
    artist_sentiment_spine_container,
    genre_emotion_spine_container,
    genre_wordcloud_container,
    sentiment_md_1,
    corr_md_1,
    tsne_container,
)

from artist_wordcloud_graphs import (
    artist_wordcloud_container, get_artist_wordcloud_callbacks
)

from ngram_wordcloud_graphs import (
    ngram_artist_wordcloud_container, get_ngram_artist_wordcloud_callbacks
)

from analysis_examples import (
    examples_md_1,
    topic_images_1,
    examples_md_2,
    topic_images_2,
    examples_md_3,
    sentiment_images,
    examples_md_4,
    unique_word_images_1,
    examples_md_5,
    unique_word_images_2,
    examples_md_6,
    meta_images
)

from introduction import (
    md_intro_1, md_intro_2, md_intro_3,
    counts_df_table, artist_df_table
)

from about import (
    about_md_1
)

from decades_analysis import (
    decade_bar_topic_container, get_decade_bar_topic_callbacks,
    decade_hist_topic_container, get_decade_hist_topic_callbacks,
    decade_metadata_container, get_decade_medatata_callbacks,
    decade_artist_metadata_container, get_decade_artist_metadata_callbacks,
    decade_corr_container,
    decade_wordcloud_container,
    decades_md_1,
    decades_md_2,
    decades_images_1
)


from scikit_ml import (
    scikit_md_1, scikit_md_2,
    scikit_ex_df_1, scikit_ex_df_2,
    scikit_md_3, scikit_md_4,
    scikit_images_1,
    scikit_md_5,
    scikit_md_6, scikit_md_7,
    scikit_ex_df_3, scikit_ex_df_4,
    scikit_md_8
)


app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

server = app.server

# ---------------------------------------------------------------------------- #
#                                  callbacks                                  #
# ---------------------------------------------------------------------------- #

get_topic_callbacks(app)
get_topic_bar_callbacks(app)
get_artist_bar_topic_callbacks(app)
get_topic_scatter_callbacks(app)
get_genre_hist_topic_callbacks(app)

get_artist_freq_dist_callbacks(app)
get_genre_freq_dist_callbacks(app)

get_genre_metadata_callbacks(app)
get_genre_hist_meta_callbacks(app)
get_artist_metadata_callbacks(app)
get_bar_line_metadata_callbacks(app)
get_bar_line_metadata_topic_callbacks(app)

get_artist_wordcloud_callbacks(app)

get_ngram_artist_wordcloud_callbacks(app)

get_decade_bar_topic_callbacks(app)
get_decade_hist_topic_callbacks(app)
get_decade_medatata_callbacks(app)
get_decade_artist_metadata_callbacks(app)



# ---------------------------------------------------------------------------- #
#                          sidebar with nav to content                         #
# ---------------------------------------------------------------------------- #

# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
# eg. margin-left is 2rem bigger than sidebar width
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

topic_graph_links = dbc.Nav([
    dbc.NavLink("Topic mentions by genre", href="#bar-topic-graph-content",
                    external_link=True),
    dbc.NavLink("Topic mentions distribution within-genre", href="#genre-hist-topic-graph-content",
                    external_link=True),
    dbc.NavLink("Topic mentions by artist", href="#artist-bar-topic-graph-content",
                    external_link=True),
    dbc.NavLink("Relations between topic mentions", href="#topic-scatter-graph-content",
                    external_link=True),
    dbc.NavLink("Artist topic mentions by year", href="#topic-graph-content",
                    external_link=True),
    dbc.NavLink("Topic mentions comparison between male and female artist", href="#topic-spine-graph-content",
                    external_link=True),
    ],
    vertical=True,
    pills=True,
)

sentiment_graph_links = dbc.Nav([
    dbc.NavLink("Sentiment split between genres", href="#genre-sentiment-spine-graph-content",
                    external_link=True),
    dbc.NavLink("Sentiment split between artists", href="#artist-sentiment-spine-graph-content",
                    external_link=True),
    dbc.NavLink("Emotional split for genres", href="#genre-emotion-spine-graph-content",
                    external_link=True),
    ],
    vertical=True,
    pills=True,
)

word_graph_links = dbc.Nav([
    dbc.NavLink("Words more common to one artist than others", href="#artist-freq-dist-graph-content",
                    external_link=True),
    dbc.NavLink("Words more common to one genre than others", href="#genre-freq-dist-graph-content",
                    external_link=True),
    dbc.NavLink("Top 20 (filtered) words by genre WordCloud'", href="#genre-wordcloud-graph-content",
                    external_link=True),
    dbc.NavLink("Dynamic top words wordcloud", href="#artist-wordcloud-graph-content",
                    external_link=True),
    dbc.NavLink("Most common ngrams for artists and genres", href="#ngram-artist-wordcloud-graph-content",
                    external_link=True),
    ],
    vertical=True,
    pills=True,
)

meta_graph_links = dbc.Nav([
    dbc.NavLink("Artist metadata by genre (mean)", href="#genre-metadata-graph-content",
                    external_link=True),
    dbc.NavLink("Metadata dristibution by genre (counts)", href="#genre-hist-meta-graph-content",
                    external_link=True),
    dbc.NavLink("Artist metadata by artist (mean)", href="#artist-metadata-graph-content",
                    external_link=True),
    dbc.NavLink("Artist metadata bar and line overlaid by year", href="#bar-line-metadata-graph-content",
                    external_link=True),
    dbc.NavLink("Genre metadata vs topical mentions", href="#bar-line-metadata-topic-graph-content",
                    external_link=True),
    ],
    vertical=True,
    pills=True,
)

corr_sne_graph_links = dbc.Nav([
    dbc.NavLink("Correlation Matrix", href="#corr-graph-content",
                    external_link=True),
    dbc.NavLink("Artist/genre t-SNE similarity", href="#tsne-graph-content",
                    external_link=True),
    ],
    vertical=True,
    pills=True,
)


static_graph_links = dbc.Nav([
    dbc.NavLink("Topical analysis", href="#examples-topical",
                    external_link=True),
    dbc.NavLink("Sentiment analysis", href="#examples-sentiment",
                    external_link=True),
    dbc.NavLink("Word-based analysis", href="#examples-words",
                    external_link=True),
    dbc.NavLink("Metadata analysis", href="#examples-meta",
                    external_link=True),
    ],
    vertical=True,
    pills=True,
)

introduction_links = dbc.Nav([
    dbc.NavLink("Home", href="#start", external_link=True),
    dbc.NavLink("Introduction", href="#md-intro", external_link=True),
    dbc.NavLink("Raw data preview", href="#counts-df", external_link=True),
    ],
    vertical=True,
    pills=True,
)

extra_links = dbc.Nav([
    dbc.NavLink("About", href="#about-extra", external_link=True),
    ],
    vertical=True,
    pills=True,
)

decade_links = dbc.Nav([
    dbc.NavLink("Topic mentions by decade for rap",
                 href="#decade-bar-topic-graph-content", external_link=True),
    dbc.NavLink("Topic mentions distribution within-decade",
                 href="#decade-hist-topic-graph-content", external_link=True),
    dbc.NavLink("Metadata by decade for rap",
                 href="#decade-metadata-graph-content", external_link=True),
    dbc.NavLink("Metadata by artist for rap decades",
                 href="#decade-artist-metadata-graph-content", external_link=True),
    dbc.NavLink("Decade correlation matrix",
                 href="#decade-corr-graph-content", external_link=True),
    dbc.NavLink("Top words by decade wordclouds",
                 href="#decade-wordcloud-graph-content", external_link=True),
    ],
    vertical=True,
    pills=True,
)

scikit_links = dbc.Nav([
    dbc.NavLink("Classification",
        href="#scikit-md-1",
        external_link=True),
    dbc.NavLink("Regression",
        href="#scikit-md-6",
        external_link=True),
    ],
    vertical=True,
    pills=True,
)


sidebar_groups = html.Div(
    dbc.Accordion(
        [
            # Introduction
            dbc.AccordionItem(
                [
                    introduction_links,
                ],
                title="Home / Introduction",
            ),
            # Interactive charts main
            dbc.AccordionItem(
                [
                    dbc.Accordion(
                        [
                        dbc.AccordionItem(
                                [
                                    topic_graph_links,
                                ],
                                title = 'Topic-based'
                            ),
                        dbc.AccordionItem(
                                [
                                    sentiment_graph_links,
                                ],
                                title = 'Sentiments and emotions'
                            ),  
                        dbc.AccordionItem(
                                [
                                    word_graph_links,
                                ],
                                title = 'Word usage'
                            ),  
                        dbc.AccordionItem(
                                [
                                    meta_graph_links,
                                ],
                                title = 'Song metadata'
                            ),  
                        dbc.AccordionItem(
                                [
                                    corr_sne_graph_links,
                                ],
                                title = 'Correlations'
                            ),  
                        ],
                    )
                ],
                title="Interactive charts",
            ),
            # Static analysis main
            dbc.AccordionItem(
                [
                    static_graph_links,
                    # extra_links,
                ],
                title="Static explaratory analysis",
            ),
            # rap Decades analysis
            dbc.AccordionItem(
                [
                    decade_links
                ],
                title="Rap music through decades",
            ),
            dbc.AccordionItem(
                [
                    scikit_links
                ],
                title = "Predicting genres"
            )
        ],
    )
)


sidebar = html.Div(
    [
        html.H2("4 worlds", className="display-4"),
        html.Hr(),
        html.P(
            "Feel free to use the navigation to jump around the project sections", 
            className="lead"
        ),
        sidebar_groups,
    ],
    style=SIDEBAR_STYLE,
)



# ---------------------------------------------------------------------------- #
#                        app content layout                                    #
# ---------------------------------------------------------------------------- #

intro_items = html.Div([
    html.H1(children='4 worlds - a look at the lyrical contents of 4 genres - a EDA project', id='start'),
    md_intro_1,
    artist_df_table,
    md_intro_2,
    counts_df_table,
    md_intro_3
])

topic_charts = html.Div([
    html.H1(children='Topical analysis'),
    topic_md_1,
    bar_topic_container,
    genre_hist_topic_container,
    artist_bar_topic_container, 
    topic_scatter_container, 
    topic_container,
    topic_spine_container,
    topic_max_md_1,
    topic_max_df_table
])

sentiment_charts = html.Div([
    html.H1(children='Sentiment / emotion analysis'),
    sentiment_md_1,
    genre_sentiment_spine_container,
    artist_sentiment_spine_container,
    genre_emotion_spine_container,
])

words_charts = html.Div([
    html.H1('Word-by-word analysis'),
    freq_md_1,
    artist_freq_dist_container,
    genre_freq_dist_container,
    genre_wordcloud_container,
    artist_wordcloud_container,
    ngram_artist_wordcloud_container,
])

meta_charts = html.Div([
    html.H1('Song metadata analysis'),
    meta_md_1,
    genre_metadata_container,
    genre_hist_metadata_container,
    artist_metadata_container,
    bar_line_metadata_container,
    bar_line_metadata_topic_container,
])

corr_sne_charts = html.Div([
    html.H1('Correlations'),
    corr_md_1,
    corr_container,
    tsne_container,
])

examples_div = html.Div([
    examples_md_1,
    topic_images_1,
    examples_md_2,
    topic_images_2,
    examples_md_3,
    sentiment_images,
    examples_md_4,
    unique_word_images_1,
    examples_md_5,
    unique_word_images_2,
    examples_md_6,
    meta_images
])

decade_items = html.Div([
    html.H1('Rap decades (1980s - 2020s) analysis'),
    decades_md_1,
    decade_bar_topic_container,
    decade_hist_topic_container,
    decade_metadata_container,
    decade_artist_metadata_container,
    decade_corr_container,
    decade_wordcloud_container,
    decades_images_1,
    decades_md_2,
])

scikit_items = html.Div([
    html.H1('Machine Learning'),
    # classification
    html.H3("Classification"),
    scikit_md_1, scikit_md_2,
    scikit_ex_df_1, scikit_ex_df_2,
    scikit_md_3, scikit_md_4,
    scikit_images_1,
    scikit_md_5,
    # regression
    html.H3("Regression"),
    scikit_md_6, scikit_md_7,
    scikit_ex_df_3, scikit_ex_df_4,
    scikit_md_8
])

content_div = html.Div([
    intro_items, html.Hr(),
    topic_charts, html.Hr(),
    sentiment_charts, html.Hr(),
    words_charts, html.Hr(),
    meta_charts, html.Hr(),
    corr_sne_charts, html.Hr(),

    html.H1(children='Examplary / static analysis'),
    examples_div,

    # about_md_1,

    decade_items, html.Hr(),

    scikit_items

], id='page-content', style=CONTENT_STYLE)

app.layout = html.Div([sidebar, content_div])

# app.run(debug=True)
if __name__ == '__main__':
    app.run_server(debug=False)
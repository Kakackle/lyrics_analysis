from dash import Dash, html, dcc, callback, Output, Input, dash_table
import dash_bootstrap_components as dbc

import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as graph_objects


import pandas as pd
import numpy as np
# Metrics for Evaluation of model Accuracy and F1-score
from sklearn.metrics  import f1_score,accuracy_score, confusion_matrix, classification_report, ConfusionMatrixDisplay
# regression metrics

# For splitting of data into train and test set
from sklearn.model_selection import train_test_split
# for categorical columns
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.metrics import mean_absolute_error, r2_score

# classification
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier

# regression
from sklearn.linear_model import LinearRegression
from xgboost.sklearn import XGBRegressor
from sklearn.svm import SVR

import matplotlib.pyplot as plt

from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

from dataframes import (
    counts_df,
    genre_mean_df,
    artist_mean_df,
    decade_counts_df,
    decade_mean_df
)

# ---------------------------------------------------------------------------- #
#                     columns to be considered for ML tasks                    #
# ---------------------------------------------------------------------------- #

counts_classif_cols = ['Year',
                      'Pageviews', 'featured_count', 'producer_count', 'writer_count',
                      'gender', 'genre', 'unique_words', 'total_words', 
                       'manual_love_count',
                       'manual_money_count', 'manual_violence_count', 'manual_drugs_count',
                       'manual_gendered_count', 'manual_sadness_count', 'manual_joy_count',
                       'manual_yes_count', 'manual_no_count',
                       'sentiment', 'emotion'
                      ]
counts_classif_cols_no_gender = [col for col in counts_classif_cols if col != 'gender']
counts_classif_cols_no_genre = [col for col in counts_classif_cols if col != 'genre']
counts_classif_cols_no_sentiment = [col for col in counts_classif_cols if col != 'sentiment']
counts_classif_cols_no_emotion = [col for col in counts_classif_cols if col != 'emotion']

# cleanup
classif_counts_df = counts_df[[*counts_classif_cols]]
classif_counts_df.dropna(inplace=True)

# ---------------------------------------------------------------------------- #
#                            model training function                           #
# ---------------------------------------------------------------------------- #

def train_classify_target(df, target_col, model, train_size=0.8, task='class'):
    """
    Takes a dataframe, target column and model,
    plus optionally train_size and tak
    
    if task set to 'class' will calculate classification metrics
    if task set to 'regr' will calculate regression metrics!
    
    creates a train-test split,
    preprocesses the (standard scaling and one-hot-encoding) pipeline,
    calculates accuracy, f1, confusion matrix metrics,
    returns the trained model and metrics

    Caveats:
        * Expects a df without NaNs, you have to choose columns / rows to drop / keep first
        * The pipeline could be expanded

    To be expanded:
        * right now takes model, could possibly take model_type and hyperparams
    
    """
    y = df[target_col]
    X = df.drop([target_col], axis=1)

    X_train, X_valid, y_train, y_valid = train_test_split(X, y, train_size=train_size, test_size=(1-train_size))

    categorical_cols = [cname for cname in X_train.columns if X_train[cname].dtype == "object"]
    numerical_cols = [cname for cname in X_train.columns if X_train[cname].dtype in ['int64', 'float64']]

    # Preprocessing transformers
    numerical_transformer = StandardScaler()
    
    categorical_transformer = Pipeline(steps=[
        ('onehot', OneHotEncoder(handle_unknown='ignore')),
    ])

    # combined preprocessor
    preprocessor = ColumnTransformer(
        transformers = [
            ('num', numerical_transformer, numerical_cols),
            ('cat', categorical_transformer, categorical_cols)
        ]
    )

    # Bundle preprocessing and modeling code in a pipeline
    train_pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('model', model)
    ])
    
    # Preprocessing of training data, fit model 
    train_pipeline.fit(X_train, y_train)

    # Preprocessing of validation data, get predictions
    preds = train_pipeline.predict(X_valid)

    # metrics
    if task == 'class':
        acc = accuracy_score(y_valid, preds)
        f1 = f1_score(y_valid, preds, average=None, labels=model.classes_)
        cm = confusion_matrix(y_valid, preds, labels=model.classes_)
        labels = model.classes_

        return {
            "acc": acc,
            "f1": f1,
            "cm": cm,
            "labels": labels,
            "model": model,
            "preds": preds,
            "X_valid": X_valid,
            "y_valid": y_valid,
            "train_pipeline": train_pipeline
            }

    if task == 'regr':
        mae = mean_absolute_error(y_valid, preds)
        r2 = r2_score(y_valid, preds)
        return {
            "mae": mae,
            "r2": r2,
            "model": model,
            "preds": preds,
            "X_valid": X_valid,
            "y_valid": y_valid,
            "train_pipeline": train_pipeline
        }
    

def save_confusion_matrix(cm, labels, exp_name):
    disp = ConfusionMatrixDisplay(confusion_matrix = cm,
                             display_labels=labels
                             )
    disp_plot = disp.plot()
    plt.savefig(f'../results/{exp_name}.png')
    # plt.show()


# ---------------------------------------------------------------------------- #
#                        classify for genre by counts_df                       #
# ---------------------------------------------------------------------------- #
    
counts_genre_model = SVC()
counts_genre_results = train_classify_target(
    df = classif_counts_df,
    target_col = 'genre',
    model = counts_genre_model
)

# print("acc: ", counts_genre_results['acc'], "f1: ", counts_genre_results['f1'])

test_index = counts_genre_results['X_valid'].head(1).index

test_counts_slice = counts_df.loc[test_index, ['Artist', 'Song Title', 'Song Lyrics', 'genre']]
test_X_valid = counts_genre_results['X_valid'].loc[test_index, :]
counts_genre_pred = counts_genre_results['train_pipeline'].predict(
    counts_genre_results['X_valid'].loc[test_index, :])

save_confusion_matrix(cm = counts_genre_results['cm'],
                      labels = counts_genre_results['labels'],
                      exp_name="counts_genre_cm"
                      )

# ---------------------------------------------------------------------------- #
#                                  explanation                                 #
# ---------------------------------------------------------------------------- #

scikit_md_1 = dcc.Markdown(
'''
    For further experiments, a few models were trained, to test the possibility
    of predicting some of the metrics considered in the analysis, based on the
    engineered variables, stemming from the data.

    This means, for both classification and tasks, only the data extracted from 
    the lyrics was used, not the lyrics themselves.

    A commonly seen method in Natural Language Processing tasks includes vectorizing long-form texts,
    such as whole song lyrics, effectively turning them into numerical vectors of large sizes,
    then using neural networks to learn the numerical relationships between them. 
    However, using only the engineered data and simpler, ML-based solutions can possibly serve
    as a testament of how well these designed statistics represent the underlying lyrics, which
    we are studying.

    As such, an example of classification learning, can be to try and predict the genre of the song,
    by the calcualted topic count, producer count etc. stats.

    Below presented are:
    * The achieved accuracy and f1 score
    * A random test song from a random genre
    * The data used to predict on this song
    * The predicted genre
    * A confusion matrix
''',
id = 'scikit-md-1'
)

scikit_md_2 = dcc.Markdown(f'Accuracy: {counts_genre_results["acc"]}, f1 score: {counts_genre_results["f1"]}')

scikit_ex_df_1 = dash_table.DataTable(
    test_counts_slice.to_dict('records'),
    columns=[{"name": c, "id": c} for c in test_counts_slice.columns],
    style_header={
        'backgroundColor': 'rgb(210, 210, 210)',
        'color': 'black',
        'fontWeight': 'bold'
    },
    style_table={"overflowX": "auto"},
    id='scikit-ex-df-1'
)

scikit_ex_df_2 = dash_table.DataTable(
    test_X_valid.to_dict('records'),
    columns=[{"name": c, "id": c} for c in test_X_valid.columns],
    style_header={
        'backgroundColor': 'rgb(210, 210, 210)',
        'color': 'black',
        'fontWeight': 'bold'
    },
    style_table={"overflowX": "auto"},
    id='scikit-ex-df-2'
)

scikit_md_3 = dcc.Markdown(f'Predicted genre: {counts_genre_pred }')
scikit_md_4 = dcc.Markdown(f'Confusion matrix:')

scikit_images_1 = html.Div([
    html.P(children='Confusion matrix', style={'textAlign': 'center'}),
    html.Img(src='assets/counts_genre_cm.png'),
])

scikit_md_5 = dcc.Markdown(
'''
    For this example the built-in scikit-learn Support Vector Classifier was used as model, with default parameters.
    Before training, any categorical variable was one-hot encoded and any numerical
    variable was passed through Scikit-learn's StandardScaler, which attempts to
    remove the mean and scales the data to unit variance.

    Such steps were taken to help aid the training and remove any skew that the different scales
    of numerical variables used could apply to the process.

    As seen, the results seem quite satisfactory, with a high accuracy rating.

    Other training tests conducted were:
    * Classification of genre based on numerical data, gender, ...
    * Classification of gender based on numerical data, genre, ... - watch out, very unbalanced
    * Classification of artist based on numerical data, genre, ...
    * Classification of genre for groupby mean data
    * Regression of unique_words, total_words, topic count etc
    * Same things for decade data except no gender and decade classification instead of genre 

    Which can be seen in a notebook called scikit_ml_attempts in the source folder in the repo
'''
)

# ---------------------------------------------------------------------------- #
#                      regress for unique_words on counts                      #
# ---------------------------------------------------------------------------- #

scikit_md_6 = dcc.Markdown(
'''
    As an example, an attempt to predict the number of unique words per song was conducted,
    using scikit-learn's implementation of Support Vector regression. The training steps taken
    were almost identical to classification, with one-hot encoding on categorical variables
    and the numerical values scaled. For result measurement the mean absolute error and a R2 score
    were calculated.

    Below presented are:
    * A random sample song to predict on
    * The values which were used for that prediction
    * The prediction and the mae and r2 scores
''',
id = 'scikit-md-6'
)

counts_unique_model = SVR()
counts_unique_results = train_classify_target(
    df = classif_counts_df,
    target_col = 'unique_words',
    model = counts_unique_model,
    task = 'regr'
)

regr_test_index = counts_unique_results['X_valid'].head(1).index

regr_test_counts_slice = counts_df.loc[regr_test_index, ['Artist', 'Song Title', 'Song Lyrics', 'unique_words']]
regr_test_X_valid = counts_unique_results['X_valid'].loc[regr_test_index, :]
counts_unique_pred = counts_unique_results['train_pipeline'].predict(
    counts_unique_results['X_valid'].loc[regr_test_index, :])

scikit_md_7 = dcc.Markdown(f'MAE: {counts_unique_results["mae"]}, \
                            r2 score: {counts_unique_results["r2"]}')

scikit_ex_df_3 = dash_table.DataTable(
    regr_test_counts_slice.to_dict('records'),
    columns=[{"name": c, "id": c} for c in regr_test_counts_slice.columns],
    style_header={
        'backgroundColor': 'rgb(210, 210, 210)',
        'color': 'black',
        'fontWeight': 'bold'
    },
    style_table={"overflowX": "auto"},
    id='scikit-ex-df-3'
)

scikit_ex_df_4  = dash_table.DataTable(
    regr_test_X_valid.to_dict('records'),
    columns=[{"name": c, "id": c} for c in regr_test_X_valid.columns],
    style_header={
        'backgroundColor': 'rgb(210, 210, 210)',
        'color': 'black',
        'fontWeight': 'bold'
    },
    style_table={"overflowX": "auto"},
    id='scikit-ex-df-4'
)

scikit_md_8 = dcc.Markdown(f'Predicted unique words: {counts_unique_pred}')



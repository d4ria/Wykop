"""Annotation file preprocessing."""
import pandas as pd
import codecs
import preprocessor as p

import re


p.set_options(p.OPT.URL, p.OPT.MENTION, p.OPT.SMILEY)


def preprocess(filepath: str):
    """Parser file for given path to json format for annotation service."""
    data = pd.read_csv(filepath)

    file = codecs.open("temp.txt", "w", "utf-8")

    for text in data['text']:
        if text:
            text = text.replace('\n', '').replace('\t', ' ')
            file.write(text+'\n')

    file.close()


def join_with_data(annotations: pd.DataFrame,
                   src_filepath: str) -> pd.DataFrame:
    """Joins annotation df with original dataset"""
    original_df = pd.read_csv(src_filepath, encoding='utf-8')
    original_df['text'] = original_df['text'].copy().apply(
        lambda x: x.replace('\xa0', ' '))
    original_df['processed_text'] = original_df['text'].copy().apply(
        lambda x: x.replace('\n', '').replace('\t', ' '))

    annotations['processed_text'] = annotations['text']
    annotations = annotations.drop(columns=['text'])

    return annotations.merge(
        original_df, how='left', on='processed_text'
        ).drop(columns='processed_text')


def prepare_dataset(annotated_data: pd.DataFrame) -> pd.DataFrame:
    """Performs operations to prepare data for classification task."""
    annotated_data = convert_to_binary_problem(annotated_data)
    voted_data = calculate_majority_vote(annotated_data)
    cleaned_data = clean_data(voted_data)

    return cleaned_data


def convert_to_binary_problem(annotated_data: pd.DataFrame) -> pd.DataFrame:
    """Deletes skip(category 3 rows) and relabels data to keep 0/1 notation"""
    skipped_examples = annotated_data[
                         annotated_data.annotation == 3
                        ].id.unique()
    annotations = annotated_data[~annotated_data.id.isin(skipped_examples)]
    assert len(annotations.annotation.unique()) == 2

    annotations.loc[annotations.annotation == 1, 'annotation'] = 0
    annotations.loc[annotations.annotation == 2, 'annotation'] = 1

    return annotations


def comment_preprocess(t: str) -> str:
    t = p.clean(t)
    t = re.sub("[^A-Za-z0-9żźćńółęąśŻŹĆĄŚĘŁÓŃ ]", "", t)
    t = re.sub(" +", " ", t)
    return t.strip()


def clean_data(data: pd.DataFrame) -> pd.DataFrame:
    """Cleans given data from url/mentions/emoticons/stopwords."""
    data['text'] = data['text'].copy().apply(lambda x: comment_preprocess(x))
    return data


def calculate_majority_vote(data: pd.DataFrame) -> pd.DataFrame:
    """For a given dataset of annotations return majority voting."""
    majority_vote = data.groupby('id').annotation.agg(
                         lambda x: x.value_counts().index[0])
    annotations = data.merge(majority_vote, on='id')

    unnecessary_columns = ['id', 'annotations', 'meta', 'annotation_approver',
                           'annotator_id', 'annotation_x', 'status',
                           'date_by_day', 'created_at_hour',
                           'created_at_weekday']
    annotations.drop(columns=unnecessary_columns, inplace=True)
    annotations.rename(columns={'annotation_y': 'annotation'}, inplace=True)
    return annotations.drop_duplicates()


if __name__ == '__main__':
    # preprocess('./data.csv')
    pass

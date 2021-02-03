import pandas as pd


def csv_to_dict(csv_file, index_col=None):
    print(f"\nConverting {csv_file} to dict...")

    df = pd.read_csv(csv_file, index_col=index_col)
    print(df)
    return df.to_dict()


def csv_to_df(csv_file, index_col=None):
    print(f"\nConverting {csv_file} to dict...")

    df = pd.read_csv(csv_file, index_col=index_col)
    print(df)
    return df


def dict_to_csv(csv_file, data_dict, sep=','):
    df = pd.DataFrame(data=data_dict)

    df_to_csv(csv_file, df, sep, index=False)


def df_to_csv(csv_file, df, sep=',', index=True):
    df.to_csv(csv_file, sep=sep, index=index)


def list_to_csv(csv_file, data_list, sep=',', excluded_columns=[]):
    data_dict = {}

    for col in range(len(data_list[0])):
        if data_list[0][col] not in excluded_columns:
            data_dict[data_list[0][col]] = []
            for row in range(len(data_list) - 2):
                data_dict[data_list[0][col]].append(data_list[row + 1][col])

    dict_to_csv(csv_file, data_dict, sep)

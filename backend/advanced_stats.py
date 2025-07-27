import pandas as pd


def add_all_adv(df):
    df = add_ts(df)
    df = add_ast_to_tov(df)
    return df

def add_ts(df):
    df["TS%"] = df.apply(
        lambda row: round(row["PTS"] / (2 * (row["FGA"] + 0.44 * row["FTA"])), 2)
                         if (row["FGA"] + 0.44 * row["FTA"]) > 0 else 0, axis=1)
    return df


def add_ast_to_tov(df):
    df["AST/TOV"] = df.apply(lambda row: row["AST"] / row["TOV"]
                             if row ["TOV"] > 0 else 0,
                             axis=1
                             )
    return df
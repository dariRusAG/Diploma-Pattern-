import pandas as pd


def get_id_favorite_pattern(conn, user_id):
    return pd.read_sql(f'''
    SELECT *
    FROM favorite
    WHERE users_id == 2
    GROUP BY pattern_id
    ''', conn)

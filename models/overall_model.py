def add_pattern(conn, user_id, pattern_id):
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO favorite(users_id, pattern_id) 
        VALUES (:user, :pattern)
    ''', {"user": user_id, "pattern": pattern_id})

    return conn.commit()


def del_pattern(conn, pattern_id):
    cur = conn.cursor()
    cur.execute(f'''
        DELETE FROM favorite
        WHERE pattern_id = :pattern;
     ''', {"pattern": pattern_id})

    return conn.commit()
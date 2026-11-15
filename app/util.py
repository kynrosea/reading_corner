
def build_sql_statement(table, values, value_names, num_required, options, option_names):
    vals = num_required
    bindings = values
    sql = f'INSERT INTO {table} ({value_names[0]}'
    for i in range(1,vals):
        sql += f', {value_names[i]}'
    
    for i, op in enumerate(options):
        if op:
            sql += f', {option_names[i]}'
            bindings.append(op)
            vals += 1

    sql += ') VALUES (?'
    for _ in range(1,vals):
        sql += ',?'

    sql += ')'

    return sql, bindings


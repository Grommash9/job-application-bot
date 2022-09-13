from bot_app.db.base import create_dict_con


async def get_all():
    con, cur = await create_dict_con()
    await cur.execute('select * from habits ')
    jobs = await cur.fetchall()
    await con.ensure_closed()
    return jobs

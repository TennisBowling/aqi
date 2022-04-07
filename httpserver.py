import sanic
import aiosqlite
from sanic import response
from datetime import datetime

app = sanic.Sanic(__name__)

@app.before_server_start
async def setup_db(app, loop):
    app.ctx.db = await aiosqlite.connect('airquality.db')
    app.ctx.db.row_factory = aiosqlite.Row

@app.before_server_stop
async def close_db(app, loop):
    await app.ctx.db.close()

@app.route('/<start:int>/<end:int>', methods=['GET'])
async def get_data(request, start: int, end: int):
    data = await app.ctx.db.execute('SELECT * FROM data WHERE "time" BETWEEN ? AND ?;', (start, end))
    rows = await data.fetchall()
    return response.json({'pm25': [float(row['pm25']) for row in rows], 'pm10': [float(row['pm10']) for row in rows], 'aqi': [float(row['aqi']) for row in rows], 'time': [row['time'] for row in rows]})

app.run('0.0.0.0', port=8080)
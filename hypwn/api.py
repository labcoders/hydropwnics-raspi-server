from . import app, HYPE_BUS

from flask import request, jsonify

def message400(message):
    return (
        jsonify(dict(message=message)),
        400,
    )

@app.route('/echo', methods=['POST'])
def echo():
    if request.method == 'POST':
        d = request.json
        b = d['value']
        b_ = HYPE_BUS.echo(b).echo
        return '{} echoed to {}'.format(b, b_)

@app.route('/light/<location>', methods=['POST', 'GET'])
def light(location):
    if location not in ('ambient', 'internal'):
        return message400('Invalid light location {}.'.format(location))

    if request.method == 'POST':
        if location == 'ambient':
            return message400('Cannot set ambient light level.')
        else:
            return light_post()
    elif request.method == 'GET':
        return light_get(location)
    else:
        raise Exception('unreachable code')

def light_post():
    r = request.json
    return jsonify(
        dict(
            ok=HYPE_BUS.set_light_level(r['state']).ok,
        ),
    )

def light_get(location):
    if location == 'ambient':
        return jsonify(
            dict(
                lightLevel=HYPE_BUS.get_light_level(location).value,
            ),
        )
    else:
        return jsonify(
            dict(
                lightLevel=HYPE_BUS.get_light_level(location).ok,
            ),
        )

@app.route('/temperature', methods=['GET'])
def temperature():
    return jsonify(
        dict(
            value=HYPE_BUS.get_temperature('ambient').value,
        ),
    )

@app.route('/pump', methods=['POST', 'GET'])
def pump():
    if request.method == 'POST':
        return pump_set()
    elif request.method == 'GET':
        return pump_get()

@app.route('/music', methods=['POST'])
def music():
    if request.method == 'POST':
        return music_set()


def pump_set():
    r = request.json
    return jsonify(
        dict(
            ok=HYPE_BUS.set_pump(r['state']).ok,
        ),
    )

def pump_get():
    return jsonify(
        dict(
            state=HYPE_BUS.get_pump().ok,
        ),
    )

def music_set():
    r = request.json
    return jsonify(
        dict(
            ok=HYPE_BUS.set_music(r['state']).ok,
        ),
    )

@app.route('/bad', methods=['POST'])
def bad():
    return jsonify(
        dict(
            ok=HYPE_BUS.bad().ok,
        ),
    )

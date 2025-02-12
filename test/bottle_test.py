import pytest
from multiprocessing import Process

from common import send_requests, mode_list, kwargs_list


def server_process(port, mode, **kwargs):
    from bottle import Bottle, run

    app = Bottle()

    @app.route('/hello/world')
    def hello():
        return 'Hello World!!!'

    if mode == 'auto':
        from swagger_ui import api_doc
        api_doc(app, **kwargs)
    else:
        from swagger_ui import bottle_api_doc
        bottle_api_doc(app, **kwargs)
    run(app, host='localhost', port=port)


@pytest.mark.parametrize('mode', mode_list)
@pytest.mark.parametrize('kwargs', kwargs_list)
def test_bottle(port, mode, kwargs):
    proc = Process(target=server_process, args=(port, mode), kwargs=kwargs)
    proc.start()
    send_requests(port, mode, kwargs)
    proc.terminate()

import dash

class WisIoHTDash(dash.Dash):
    def interpolate_index(self, **kwargs):
        return '''<!DOCTYPE html>
        <html>
            <head>
                <title>Title</title>
            </head>
            <body>
                <div id="custom-header">{{{ g.user['email'] }}}</div>
                    {app_entry}
                    {config}
                    {scripts}
                    {renderer}
                <div id="custom-footer">My custom footer</div>
            </body>
        </html>'''.format(app_entry=kwargs.get('app_entry'),
                          config=kwargs.get('config'),
                          scripts=kwargs.get('scripts'),
                          renderer=kwargs.get('renderer'))

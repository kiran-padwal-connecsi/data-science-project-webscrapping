from AppModel import AppModel


class MyController:

    def monitor(self):
        my_app = AppModel()
        url_content = my_app.read()
        my_app.get_response(url_content)

#con = MyController()
#con.monitor()
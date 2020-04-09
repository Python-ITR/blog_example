from flask import Flask, Response, request

from services import SessionsService, UsersService


def register_middlewaries(app: Flask):
    @app.after_request
    def attach_session(res: Response):
        """
        Прикрекпляет session_token(Кука) к сессии если он отсутствует
        Если аргемент force равен 'True' - мы принудительно создаем новую запись сессии в БД
        """
        st = request.cookies.get(app.config.get("SESSION_COOKIE", ""))
        if not st:
            session = SessionsService.create_new_session()
            res.set_cookie(app.config.get("SESSION_COOKIE"), session.token)
        else:
            session = SessionsService.get_session_by_token(st)
            if not session:
                session = SessionsService.create_new_session()
                res.set_cookie(app.config.get("SESSION_COOKIE"), session.token)
        return res

    @app.before_request
    def get_user():
        request.user = None
        request.session_token = None
        st = request.cookies.get(app.config.get("SESSION_COOKIE", ""))
        if st:
            request.session_token = st
            session = SessionsService.get_session_by_token(st)
            if session:
                if session.user_id:
                    user = UsersService.get_user_by_id(session.user_id)
                    request.user = user

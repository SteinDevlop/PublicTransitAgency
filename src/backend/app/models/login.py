from starlette.requests import Request

class LoginForm:
    def __init__(self, request: Request):
        self.request = request
        self.username: str = ""
        self.password: str = ""
        self.errors = []

    async def load_data(self):
        form = await self.request.form()
        self.username = form.get("username")
        self.password = form.get("password")

    async def is_valid(self):
        if not self.username or not self.password:
            self.errors.append("Both fields are required.")
            return False
        return True

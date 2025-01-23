from locust import task, FastHttpUser
from insert_product import login
from http.cookiejar import Cookie

class AddToCart(FastHttpUser):
    host = "http://localhost:5000"
    default_headers = {
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-US,en;q=0.5",
        "Connection": "keep-alive",
        "DNT": "1",
        "Sec-GPC": "1",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0",
    }

    def __init__(self, environment):
        super().__init__(environment)
        self.username = "test123"
        self.password = "test123"
        cookies = login(self.username, self.password)
        self.token = cookies.get("token")
        
        # Create a cookie and add it to the cookiejar
        token_cookie = Cookie(
            version=0,
            name="token",
            value=self.token,
            port=None,
            port_specified=False,
            domain="localhost",
            domain_specified=False,
            domain_initial_dot=False,
            path="/",
            path_specified=True,
            secure=False,
            expires=None,
            discard=True,
            comment=None,
            comment_url=None,
            rest={},
            rfc2109=False,
        )
        self.client.cookiejar.set_cookie(token_cookie)

    @task
    def t(self):
        with self.client.get(
            "/cart",
            headers={
                **self.default_headers,
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8",
                "Host": "localhost:5000",
                "Priority": "u=0, i",
                "Referer": "http://localhost:5000/product/1",
                "Sec-Fetch-Dest": "document",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-Site": "same-origin",
                "Sec-Fetch-User": "?1",
                "Upgrade-Insecure-Requests": "1",
            },
            catch_response=True,
        ) as resp:
            pass


if __name__ == "__main__":
    run_single_user(AddToCart)

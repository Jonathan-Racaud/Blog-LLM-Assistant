import http.server
import socketserver
import os
import subprocess
import time

from urllib.parse import parse_qs

PORT = 3050
OUTPUT_DIR = "output"
IMAGE_FILE = os.path.join(OUTPUT_DIR, "image.png")

class ArticleRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(self.generate_page().encode("utf-8"))
        elif self.path.startswith("/output/image.png"):
            try:
                with open(IMAGE_FILE, "rb") as f:
                    self.send_response(200)
                    self.send_header("Content-type", "image/png")
                    self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
                    self.end_headers()
                    self.wfile.write(f.read())
            except FileNotFoundError:
                self.send_error(404, "Image not found.")
        else:
            super().do_GET()

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        parsed = parse_qs(post_data.decode('utf-8'))
        article_text = parsed.get("article", [""])[0]

        # Save input
        with open("input.txt", "w", encoding="utf-8") as f:
            f.write(article_text)

        # Call the external script
        subprocess.run(["python3", "generate_article.py", article_text])

        # Redirect back to main page
        self.send_response(303)
        self.send_header("Location", "/")
        self.end_headers()

    def generate_page(self):
        title = read_output("title.txt")
        description = read_output("description.txt")
        improved = read_output("feedback.txt")
        timestamp = int(time.time())  # To force image refresh

        return f"""
        <html>
        <head>
            <title>Article Generator</title>
            <meta http-equiv="refresh" content="10">
            <link
  rel="stylesheet"
  href="https://cdn.jsdelivr.net/npm/@picocss/pico@2/css/pico.min.css"
>
            <style>
                body {{ padding: 50; }}
                textarea {{ width: 100%; height: 250px; }}
                img {{ max-width: 100%; height: auto; }}
            </style>
        </head>
        <body>
            <h1>Writer assistant</h1>
            <h3>Generate article's title, description, image and get feedback</h3>
            <form method="POST">
                <textarea name="article"></textarea><br>
                <button type="submit">Generate</button>
            </form>

            <div class="output">
                <h2>{title}</h2>
                <p><strong>Description:</strong> {description}</p>
                <p><strong>Feedback:</strong><br>{improved.replace('\n', '<br>')}</p>
                <img src="/output/image.png?ts={timestamp}" alt="Generated image">
            </div>
        </body>
        </html>
        """

def read_output(filename):
    path = os.path.join(OUTPUT_DIR, filename)
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read().strip()
    return ""

if __name__ == "__main__":
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with socketserver.TCPServer(("", PORT), ArticleRequestHandler) as httpd:
        print(f"Serving at http://localhost:{PORT}")
        httpd.serve_forever()

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl

class UNIMAWebBrowser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("UNIMA Web Browser")
        self.setGeometry(100, 100, 1000, 700)

        self.webview = QWebEngineView()
        self.input = QLineEdit()
        self.button = QPushButton("Go")

        self.input.setPlaceholderText("Enter page name (e.g., index, register)")
        self.button.clicked.connect(self.load_page)

        layout = QVBoxLayout()
        layout.addWidget(self.input)
        layout.addWidget(self.button)
        layout.addWidget(self.webview)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.webview.load(QUrl("http://localhost:8085/"))

    def load_page(self):
        page = self.input.text().strip()
        if not page:
            page = "index"

        url = QUrl(f"http://localhost:8085/{page}")
        self.webview.load(url)
        self.webview.loadFinished.connect(self.check_page_loaded)

    def check_page_loaded(self, success):
        self.webview.loadFinished.disconnect(self.check_page_loaded)
        if not success:
            query = self.input.text().strip()
            google_url = f"https://www.google.com/search?q={query}"
            html = f"""
            <html>
                <head><title>Page Not Found</title></head>
                <body style='font-family: Arial; text-align: center; padding-top: 50px;'>
                    <h2>Document Not Found</h2>
                    <p>The page '<strong>{query}</strong>' could not be found on the local server.</p>
                    <p>You can try searching for it on Google:</p>
                    <p><a href="{google_url}" target="_blank">Search Google for "{query}"</a></p>
                </body>
            </html>
            """
            self.webview.setHtml(html)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    browser = UNIMAWebBrowser()
    browser.show()
    sys.exit(app.exec_())

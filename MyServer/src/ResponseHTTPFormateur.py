import os
import subprocess
import uuid
from urllib.parse import urlparse
from http.cookies import SimpleCookie


class ResponseHTTPFormateur:

    def __init__(self) -> None:
        self.tab_content_type = {
            # Textes
            ".php": "text/html",
            ".css": "text/css",
            ".jsp": "text/html",
            ".js": "text/javascript",
            # Images
            ".jpeg": "image/jpeg",
            ".jpg": "image/jpeg",
            ".png": "image/png",
            ".gif": "image/gif",
            ".bmp": "image/bmp",
            ".webp": "image/webp",
            ".svg": "image/svg+xml",
            ".ico": "image/x-icon",
            ".tiff": "image/tiff",
            ".heic": "image/heic",
            # Musiques
            ".mp3": "audio/mpeg",
            ".wav": "audio/wav",
            ".ogg": "audio/ogg",
            ".flac": "audio/flac",
            ".aac": "audio/aac",
            ".m4a": "audio/mp4",
            # Vidéos
            ".mp4": "video/mp4",
            ".mov": "video/quicktime",
            ".avi": "video/x-msvideo",
            ".mkv": "video/x-matroska",
            ".webm": "video/webm",
            ".flv": "video/x-flv",
            ".wmv": "video/x-ms-wmv",
            ".3gp": "video/3gpp",
            ".mpeg": "video/mpeg"
        }
        self.projects_path = "./www"
        self.sessions = {}

    def generate_session_id(self):
        return str(uuid.uuid4())

    def get_session(self, cookies):
        session_id = cookies.get("SESSIONID")
        if session_id and session_id in self.sessions:
            return session_id, self.sessions[session_id]
        else:
            session_id = self.generate_session_id()
            self.sessions[session_id] = {}
            return session_id, self.sessions[session_id]

    def delete_file(path):
        """
        Supprime un fichier donné.
        :param chemin_fichier: Chemin complet ou relatif du fichier à supprimer.
        :return: Un message indiquant le résultat de l'opération.
        """
        try:
            # Vérifie si le fichier existe
            if os.path.isfile(path):
                os.remove(path)
                return True
            else:
                return False
        except Exception as e:
            return f"Une erreur s'est produite lors de la suppression du fichier : {e}"

    def parse_cookies(self, headers):
        cookie_header = [header for header in headers.split(
            "\r\n") if header.startswith("Cookie:")]
        if cookie_header:
            cookie = SimpleCookie(cookie_header[0].split(": ", 1)[1])
            return {key: morsel.value for key, morsel in cookie.items()}
        return {}

    def get_common_headers(self, content_type, content_length, session_id):
        headers = (
            f"Content-Type: {content_type}\r\n"
            f"Connection: close\r\n"
            f"Content-Length: {content_length}\r\n"
            f"Cache-Control: no-cache, no-store, must-revalidate\r\n"
            f"Pragma: no-cache\r\n"
            f"Expires: 0\r\n"
        )
        if session_id:
            headers += f"Set-Cookie: SESSIONID={session_id}; HttpOnly\r\n"
        return headers

    def list_files(self, path):
        urls = (path.split("\\")[len(path.split("\\")) - 1]).split('/')
        urls.reverse()
        urls.append(urls[0])
        urls.pop(0)
        urls.reverse()
        # urls[0], urls[len(urls) - 1] = urls[len(urls) - 1], urls[0]
        nav = "<p>"
        i = 0
        for url in urls:
            j = 0
            if url == "":
                nav += "> <a href = '/' > Accueil </a> "
            else:
                urI = ""
                while i >= j:
                    urI += ("/" + urls[j])
                    j += 1
                nav += "> <a href = '/"+urI+"' > " + url + " </a> "
            i += 1
        nav += "</p>"
        # for url in urls:
            # print("url : " + url)
        files = os.listdir(path)
        # print(files)
        file_list_html = "\n".join(
            f"<li><a href='{file}/'>"
            f"<span style='font-size: 25px;'>&#128193;</span> {file}/</a></li>"
            if os.path.isdir(os.path.join(path, file))
            else f"<li><a href='{file}'>"
            f"<span style='font-size: 25px;'>"
            f"{'&#128187;' if file.endswith(('.php', '.html', '.js','.css')) else '&#128247;' if file.endswith(('.jpg', '.png', '.gif','.jpeg')) else '&#128196;'}</span> {file}</a></li>"
            for file in files
        )

        return f"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width,
                initial-scale=1.0">
                <title>My Server HTTP</title>
                <style>
                    body {{
                        font-family: 'Gill Sans', 'Gill Sans MT', Calibri,
                        'Trebuchet MS', sans-serif;
                    }}
                    a {{
                        text-decoration: none;
                        color: black;
                    }}
                    a:hover {{
                        color: blue;
                    }}
                    li {{
                        list-style: none;
                        padding: 7px;
                    }}
                    .fa-folder {{
                        color: gold;
                    }}
                    .fa-file {{
                        color: rgb(195, 47, 47);
                    }}
                    .fa-file-image {{
                        color: rgb(173, 145, 255);
                    }}
                    .fa-file-code {{
                        color: rgb(0, 135, 108);
                    }}
                </style>
            </head>
            <body>
                <h1>My Server HTTP</h1>
                {nav}
                <ul>
                    {file_list_html}
                </ul>
            </body>
            </html>
            """

    def chercher_fichiers_par_nom(self, dossier, debut_nom):
        fichiers = os.listdir(dossier)  # Liste tous les fichiers/dossiers
        resultats = [
            f for f in fichiers
            # On ne prend que les .php et .html
            if f.startswith(debut_nom) and (f.endswith(".php")
                                            or f.endswith(".html"))
        ]
        return resultats

    def get_HTTP_response(self, requete_HTTP,adresse_IP):
        # print(f"Requête HTTP reçue : {requete_HTTP}")

        try:
            request_line = requete_HTTP.split("\r\n")[0]
            method, path, _ = request_line.split()
            
            headers = requete_HTTP.split("\r\n\r\n")[0]
            cookies = self.parse_cookies(headers)

            session_id, session_data = self.get_session(cookies)

            from src.package.Function import write_file
            write_file("./log/access.log",f" {adresse_IP} --'{request_line}'")
            
            #print(self.get_session(cookies))

        except ValueError:
            from src.package.Function import write_file
            write_file("./log/error.log",f" [error] [{adresse_IP}] Bad Request")
            return {"tete": "HTTP/1.1 400 Bad Request\r\n\r\n", "body": ""}
            

        parsed_url = urlparse(path)
        file_path = os.path.join(self.projects_path, parsed_url.path.lstrip("/"
                                                                            ))
        _, extension = os.path.splitext(file_path)

        if os.path.isdir(file_path):
            # Verfie si en trouve des fichier index
            if len(self.chercher_fichiers_par_nom(file_path, "index")) > 0:
                fichiers = self.chercher_fichiers_par_nom(file_path, "index")
                nouvelle_requete = f"GET {path}{fichiers[0]} HTTP/1.1"
                return self.get_HTTP_response(nouvelle_requete,adresse_IP)

            # Sinon en affiche la liste des fichier dans le dossier
            response_body = self.list_files(file_path).encode('utf-8')
            response_headers = self.get_common_headers(
                "text/html", len(response_body), session_id)
            response = f"HTTP/1.1 200 OK\r\n{response_headers}\r\n"
            return {"tete": response, "body": response_body}

        elif os.path.exists(file_path):
            # Si le fichier est .php ou .html, passez-le à PHP
            # Misy modification
            if extension in [".php", ".html"]:
                result = subprocess.run(
                    ["php", "-l", file_path],
                    capture_output=True,
                    text=True
                )
                if result.returncode != 0:
                    from src.package.Function import write_file
                    write_file("./log/error.log",f" [error] [{adresse_IP}] {result.stderr.strip()}")

                if method == "POST":
                    file_name = file_path.replace("\\", "/")
                    body = requete_HTTP.split("\r\n\r\n")[
                        1] if "\r\n\r\n" in requete_HTTP else ""
                    prompt = "php -r \"parse_str('{body}',$_POST); include '{file_path}';\"".format(
                        body=body, file_path=file_name)
                    process = subprocess.run(
                        prompt,
                        shell=True,
                        capture_output=True,
                        text=True
                    )

                    response_body = process.stdout

                elif method == "GET":
                    file_name = file_path.replace("\\", "/")
                    prompt = "php -r \"parse_str('{body}',$_GET); include '{file_path}';\"".format(
                        body=parsed_url.query, file_path=file_name)
                    process = subprocess.run(
                        prompt,
                        shell=True,
                        capture_output=True,
                        text=True
                    )

                    response_body = process.stdout
                else:
                    process = subprocess.run(
                        ["php", file_path],  # Exécuter PHP
                        capture_output=True,
                        text=True,
                        env=os.environ
                    )
                    response_body = process.stdout.encode('utf-8')
                content_type = "text/html"
# Eto n farany modification
            else:
                # Pour les autres types de fichiers, lire le contenu brut
                with open(file_path, "rb") as f:
                    response_body = f.read()
                content_type = self.tab_content_type.get(
                    extension, "application/octet-stream")

            response_headers = self.get_common_headers(
                content_type, len(response_body), session_id)
            response = f"HTTP/1.1 200 OK\r\n{response_headers}\r\n"
            return {"tete": response, "body": response_body}

        else:
            response_body = b"<h1>404 Not Found</h1>"
            response_headers = self.get_common_headers(
                "text/html", len(response_body), session_id)
            response = f"HTTP/1.1 404 Not Found\r\n{response_headers}\r\n"
            from src.package.Function import write_file
            file_path =file_path.replace("\\","/")
            write_file("./log/error.log",f" [error] [{adresse_IP}] File does not exist:{file_path}")
            return {"tete": response, "body": response_body}

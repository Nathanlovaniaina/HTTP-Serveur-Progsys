import socket
import threading
import xml.etree.ElementTree as ET
from src.ResponseHTTPFormateur import ResponseHTTPFormateur
from src.package.Function import write_file

class Server:
    def __init__(self, config_path="config.xml"):
        self.root_dir = "./www"
        self.port = 3355
        self.config_path = config_path
        self.running = False  # Indique si le serveur est en cours d'exécution
        self.server_socket = None
        self.load_config()

    def load_config(self):
        """Load server configurations from an XML file."""
        try:
            tree = ET.parse(self.config_path)
            root = tree.getroot()
            self.root_dir = root.find("root_dir").text
            self.port = int(root.find("port").text)
        except Exception as e:
            write_file("./log/error.log", " [error] [local] Server configuration issue")
            print(f"Erreur de lecture du fichier configuration ({self.config_path}) : {e}")

    def handle_client(self, client_socket, address):
        """Handle a single client connection."""
        try:
            request = client_socket.recv(1024).decode()
            if not request:
                client_socket.close()
                return

            interpreteur = ResponseHTTPFormateur()
            interpreteur.projects_path = self.root_dir
            response = interpreteur.get_HTTP_response(request, address[0])
            tete = response.get("tete")
            body = response.get("body")

            client_socket.send(tete.encode())
            write_file("./log/response.log", f"\n\n\n\n\n\n\n\n [RESPONSE] \n --EN TETE \n {tete} ")
            write_file("./log/response.log", f"  --BODY \n {body}")
            if isinstance(body, str):
                client_socket.send(body.encode('utf-8'))
            else:
                client_socket.send(body)
        except Exception as e:
            write_file("./log/error.log", f" [error] [{address[0]}] Erreur dans la communication entre le serveur et le client")
            #print(f"Erreur test : {e.__dict__}")
        finally:
            client_socket.close()

    def start(self):
        """Start the server and listen for incoming connections."""
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(("0.0.0.0", self.port))
        self.server_socket.listen(5)
        self.running = True
        print(f"Serveur démarré sur le port {self.port}...")

        try:
            while self.running:
                # Timeout pour permettre l'arrêt propre
                self.server_socket.settimeout(1)
                try:
                    client_socket, addr = self.server_socket.accept()
                    write_file("./log/log.txt", f"Connexion reçue de {addr}")
                    client_thread = threading.Thread(target=self.handle_client, args=(client_socket, addr))
                    client_thread.start()
                except socket.timeout:
                    continue
        except Exception as e:
            write_file("./log/error.log", f" [error] [local] Serveur interrompu : {e}")
            #print(f"Erreur : {e}")
        finally:
            self.server_socket.close()
            print("Serveur arrêté.")

    def stop(self):
        """Stop the server."""
        self.running = False
        if self.server_socket:
            self.server_socket.close()
        print("Commande d'arrêt du serveur reçue.")

# Exemple d'utilisation
if __name__ == "__main__":
    server = Server()

    # Lancer le serveur dans un thread séparé
    server_thread = threading.Thread(target=server.start)
    server_thread.start()

    # Exemple d'arrêt du serveur après 10 secondes
    import time
    time.sleep(10)
    server.stop()
    server_thread.join()

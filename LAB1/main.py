import web_serv
import client_serv

def main():
    entry=input("Bienvenido, seleccione lo necesario. \n1. Server. \n2. Client. \n")
    if(entry=="1"):
        server = web_serv.Web(8182, "127.0.0.1")
        server.web_start()
    elif(entry=="2"):
        print("Entro al menu")
        user = client_serv.Client(8182,"127.0.0.1")
        user.clientStart()


if __name__ == "__main__":
    main()
    
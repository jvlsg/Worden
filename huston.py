from src.app import HustonApp
# from src.api import Api_Manager

def main():
    App = HustonApp()
    # api_man = Api_Manager(App) #TODO: Possibly Have the threads here and the API Man and the App communicating indirectly
    App.run()
    

if __name__ == "__main__":
    main()

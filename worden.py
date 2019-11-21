from src.app import WordenApp
# from src.api import Api_Manager

def main():
    App = WordenApp()
    # api_man = Api_Manager(App) #TODO: Possibly Have the threads here and the API Man and the App communicating indirectly
    App.run()
    

if __name__ == "__main__":
    main()

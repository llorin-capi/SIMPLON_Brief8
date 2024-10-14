from services import jcdecaux_services as jcds

if __name__ == '__main__':
    stations = jcds.get_stations()
    print(stations)

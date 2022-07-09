from xml.dom.pulldom import parseString
from owlready2 import *
import pandas as pd
import ast
import csv

owlready2.JAVA_EXE = "C:\Program Files\Java\jdk-16.0.1\\bin\java.exe"

onto = get_ontology('http://example.rouen/ontology.owl')

with onto:
    class User(Thing):
        pass

    class PointsOfInterest(Thing): pass

    class Types(Thing): 
        pass

    class Events(Thing):
        pass

    AllDisjoint([User, Types, PointsOfInterest, Events])

    class isTypeof(PointsOfInterest >> Types): 
        pass

    class isEventofPOI(ObjectProperty): pass
    class hasEvent(ObjectProperty): 
        domain = [PointsOfInterest]
        range = [Events]
        inverse_property = isEventofPOI

    class isPreferenceofUser(ObjectProperty): pass
    class hasUserPreference(ObjectProperty): 
        domain = [User]
        range = [PointsOfInterest]
        inverse_property = isPreferenceofUser

    class hasName(DataProperty):
        domain = [PointsOfInterest]
        range = [str]

    class hasRating(PointsOfInterest >> float, FunctionalProperty):
        pass

    class isLocatedAt(PointsOfInterest >> str, FunctionalProperty):
        pass

    class hasLatitude(PointsOfInterest >> float, FunctionalProperty):
        pass

    class hasLongitude(PointsOfInterest >> float, FunctionalProperty):
        pass

    class hasTime(User >> str, FunctionalProperty):
        pass

    class hasWeather(User >> str, FunctionalProperty):
        pass

    class hasTransport(User >> bool, FunctionalProperty):
        pass

    class hasScore(DataProperty, FunctionalProperty):
        domain = [PointsOfInterest]
        range = [float]

    class hasInterestScore(DataProperty, FunctionalProperty):
        domain = [PointsOfInterest]
        range = [float]

    class hasConfidenceScore(DataProperty, FunctionalProperty):
        domain = [PointsOfInterest]
        range = [float]

    class nature(Types): pass
    class history(Types): pass
    class architecture(Types):pass 
    class lodging(Types): pass
    class bakery(Types):pass
    class food(Types): pass
    class store(Types): pass
    class restaurant(Types): pass
    class park(Types): pass
    class bar(Types): pass
    class movie_theater(Types): pass
    class church(Types): pass
    class place_of_worship(Types): pass
    class art_gallery(Types): pass
    class museum(Types): pass
    class cafe(Types): pass
    class night_club(Types): pass
    class gym(Types): pass
    class spa(Types): pass
    class library(Types): pass
    class campground(Types): pass
    class shopping_mall(Types): pass
    class synagogue(Types): pass
    class mosque(Types): pass
    class casino(Types): pass
    class bowling_alley(Types): pass
    class stadium(Types): pass
    class tourist_attraction(Types): pass
    class bike_sharing(Types): pass
    class tea_house(Types): pass
    class landmark_and_historical_building(Types): pass
    class pub(Types): pass
    
    # High level POI
    

    # class Art(PointsOfInterest): pass
    class Nature(PointsOfInterest): 
         equivalent_to = [PointsOfInterest & isTypeof.some(nature)]
    class Cuisine(PointsOfInterest): pass
    class Cultural(PointsOfInterest): 
        equivalent_to = [PointsOfInterest & isTypeof.some(tourist_attraction)]
    class History(PointsOfInterest): 
        equivalent_to = [PointsOfInterest & isTypeof.some(landmark_and_historical_building or history)]
    class NightLife(PointsOfInterest): pass
    class Entertainment(PointsOfInterest):pass
    # class Store(PointsOfInterest):
    #     equivalent_to = [PointsOfInterest & isTypeof.some(store)]

    # 2nd level POIs
    class Sport(Entertainment): pass

    class Art_gallery(Cultural):
        equivalent_to = [PointsOfInterest & isTypeof.some(art_gallery)]

    class Park(Nature): 
        equivalent_to = [PointsOfInterest & isTypeof.some(park)]
    
    class Bike_Sharing(Nature):
        equivalent_to = [PointsOfInterest & isTypeof.some(bike_sharing)]

    class Museum(Cultural): 
        equivalent_to = [PointsOfInterest & isTypeof.some(museum)]

    class Library(Entertainment): 
        equivalent_to = [PointsOfInterest & isTypeof.some(library)]
    Library.is_a.append(Cultural)

    class Restaurant(Cuisine): 
        equivalent_to = [PointsOfInterest & isTypeof.some(restaurant)]
    
    class Tea_House(Cuisine):
        equivalent_to = [PointsOfInterest & isTypeof.some(tea_house)]

    class Bakery(Cuisine):
        equivalent_to = [PointsOfInterest & isTypeof.some(bakery)]
 
    class Bar(NightLife): 
        equivalent_to = [PointsOfInterest & isTypeof.some(bar or pub)]


    class Bowling_alley(Entertainment): 
        equivalent_to = [PointsOfInterest & isTypeof.some(bowling_alley)]
    # Bowling_alley.is_a.append(Sport)

    class Cafe(Cuisine):
        equivalent_to = [PointsOfInterest & isTypeof.some(cafe)]

    class Church(Cultural):
        equivalent_to = [PointsOfInterest & isTypeof.some(church)]
    class Synagogue(Cultural):
        equivalent_to = [PointsOfInterest & isTypeof.some(synagogue)]
    class Mosque(Cultural): 
        equivalent_to = [PointsOfInterest & isTypeof.some(mosque)]

    class Gym(Sport):
        equivalent_to = [PointsOfInterest & isTypeof.some(gym)]

    class Stadium(Sport):
        equivalent_to = [PointsOfInterest & isTypeof.some(stadium)]

    class Night_club(NightLife):
        equivalent_to = [PointsOfInterest & isTypeof.some(night_club)]

    class Spa(Entertainment):
        equivalent_to = [PointsOfInterest & isTypeof.some(spa)]
    # Spa.is_a.append(Sport)

    class Theater(Entertainment):
        equivalent_to = [PointsOfInterest & isTypeof.some(movie_theater)]

    class Casino(Entertainment):
       equivalent_to = [PointsOfInterest & isTypeof.some(casino)]
    Casino.is_a.append(NightLife)

    class NatureMuseum(Museum):
        equivalent_to = [Museum & isTypeof.some(nature)]
    NatureMuseum.is_a.append(Nature)

    class HistoryMuseum(Museum):
        equivalent_to = [Museum & isTypeof.some(history)]
    HistoryMuseum.is_a.append(History)

    class ArchitectureMuseum(Museum):
        equivalent_to = [Museum & isTypeof.some(architecture)]


if __name__ == '__main__':
    file = open('point_of_interests.csv',  encoding="utf-8")
    reader = csv.reader(file)
    next(reader)
    with onto:
        for row in reader:
            place_id, place_name, type1, type2, type3, price_level, average_rating, user_ratings_total, formatted_address,\
            latitude, longitude,  geohash,upper_geohash, distance, duration = row

            if type1 == 'shopping':
                continue

            individual = onto.PointsOfInterest(place_id)

            if place_name:
                individual.hasName = [place_name]

            if type2:
                try:
                    place_type = onto[type2]
                    type_individual = place_type(f'indv_{type2}')
                    individual.isTypeof.append(type_individual)
                except: pass
            
            if type3:
                type3 = ast.literal_eval(type3)
                try:
                    for types in type3:
                        place_type = onto[types]
                        type_individual = place_type(f'indv_{types}')
                        individual.isTypeof.append(type_individual)
                except: pass

            if formatted_address:
                individual.isLocatedAt = formatted_address
            
            if latitude:
                individual.hasLatitude = float(latitude)
            
            if longitude:
                individual.hasLongitude = float(longitude)

            if average_rating:
                individual.hasRating = float(average_rating)

                    
        sync_reasoner_pellet()
        onto.save('rouen_ontology.owl')












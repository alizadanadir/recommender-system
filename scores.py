from owlready2 import *
from rouen_ontology import *
from context import *
import math
import csv

onto = get_ontology('rouen_ontology.owl').load()

    
user1 = User('some_user')
user1.hasTime = current_time
user1.hasWeather = current_weather
user1.hasTransport = False
user_location = [49.4445941,  1.1001238]

input_scores = {}
high_classes = [Nature, Cuisine, Cultural, History, NightLife, Entertainment]

class Scores:
    def __init__(self, input_scores):
        self.input_scores = input_scores

    def user_input(self):
        for i in range(len(high_classes)):
            while True:
                value = float(input(f'How interested you are in {high_classes[i]}?\n'))
                if int(value) not in range(1, 11):
                    continue
                break
            input_scores[high_classes[i]] = value

    
    def to_csv(self, data):
        try:
            with open('results.csv','w', encoding = 'ISO-8859-1') as out:
                csv_out=csv.writer(out)
                csv_out.writerow(['place','type', 'score'])
                for row in data:
                    csv_out.writerow(row)
        except: 
            with open('results.csv','w', encoding = 'utf-8') as out:
                csv_out=csv.writer(out)
                csv_out.writerow(['place','type', 'score'])
                for row in data:
                    csv_out.writerow(row)
            
    
    def output(self, result):
        for i in range(len(result)):
            print(i+1,':', result[i])

    def get_hierarchy(self):
        classes = []
        for cl in PointsOfInterest.subclasses():
            classes.append(cl)

        for cl in PointsOfInterest.subclasses():
            for j in cl.subclasses():
                    if j not in classes:
                        classes.append(j)

        for cl in PointsOfInterest.subclasses():
            for j in cl.subclasses():
                    if j not in classes:
                        for k in j.subclasses():
                            if k not in classes:
                                classes.append(k)
        return classes



    def interestscore(self, current_class):
        if current_class in self.input_scores:
            return self.input_scores[current_class]
        
        ancestors = current_class.ancestors()
        score = 0
        divisor = 0
        for i in ancestors:
            if i not in [current_class, PointsOfInterest, Thing]:
                score += self.interestscore(i) * self.confidencescore(i)
                divisor += self.confidencescore(i)      
        return score/divisor
        

    def confidencescore(self,current_class):
        max_value = 10
        if current_class in self.input_scores:
            return max_value

        ancestors = current_class.ancestors()
        for i in ancestors:
            if i not in [current_class, PointsOfInterest, Thing]:
                score = self.confidencescore(i)
                if max_value > score:
                    max_value = score
                score = max_value - 1
        return score


    def scores(self):
        classes = self.get_hierarchy()
        for class_n in classes:
            for instance in class_n.instances():
                instance.hasInterestScore = self.interestscore(class_n)
                instance.hasConfidenceScore = self.confidencescore(class_n)

        for i in PointsOfInterest.instances():
            if i.hasInterestScore:
                i.hasScore = i.hasInterestScore * i.hasConfidenceScore



    def haversine_distance(self, point1, point2):
        lat1, lon1 = point1
        lat2, lon2 = point2
        
        earth_radius = 6371 # km
        f1 = lat1 * math.pi/180
        f2 = lat2 * math.pi/180

        f = (lat2 - lat1) * math.pi/180
        l = (lon2 - lon1) * math.pi/180

        a = math.sin(f/2) * math.sin(f/2) + math.cos(f1) * math.cos(f2) * math.sin(l/2) * math.sin(l/2)

        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

        return earth_radius * c



    def distance_to_time(self, distance):
        return distance * 12 # 1 km is +- 12 minutes of walk according to Google Maps

    # need to change this
    def distance_score(self,user_location):     
        for instance in set(PointsOfInterest.instances()):
            if instance.hasScore:
                instance_location = [instance.hasLatitude, instance.hasLongitude]
                distance = self.haversine_distance(user_location, instance_location) 
                time = int(self.distance_to_time(distance))
                if user1.hasTransport:
                    time = int(time/3)
                else: pass
                if time in range(0,15):
                    instance.hasScore = 1.2 * instance.hasScore 
                elif time in range(30, 60):
                    instance.hasScore = 0.8 * instance.hasScore
                elif time in range(60, 99999):
                    instance.hasScore = 0.5 * instance.hasScore
                else:
                    pass


    def time_context(self,user1):
        if  user1.hasTime == 'lunchtime':
            for instance in set(Cuisine.instances()):
                instance.hasScore =  1.6 * instance.hasScore
            for instance in set(Cultural.instances()):
                instance.hasScore = 1.5 * instance.hasScore

        elif user1.hasTime == 'nighttime':
            for instance in set(NightLife.instances()):
                instance.hasScore =  1.4 * instance.hasScore
            for instance in set(Cultural.instances()):
                instance.hasScore = 0.7 * instance.hasScore

        elif user1.hasTime == 'daytime':
            for instance in set(NightLife.instances()): 
                instance.hasScore = 0.6 * instance.hasScore
            for instance in set(Cultural.instances()):  
                instance.hasScore  =  1.3 * instance.hasScore


    def weather_context(self,user1):
        if user1.hasWeather in ['rainy', 'snow', 'drizzle', 'thunderstorm']:
            for instance in set(Nature.instances()): 
                instance.hasScore = 0.35 * instance.hasScore
        else:
            for instance in set(Nature.instances()):
                instance.hasScore = 1.2 * instance.hasScore

    def context(self):
        self.time_context(user1)
        self.weather_context(user1)

    def normalize_scores(self, current_results):
        for i in range(len(current_results)):
            current_results[i] = list(current_results[i])

        max_value = current_results[0][2]
        current_results[0][2] = 100
        for i in range(1, len(current_results)):
            current_results[i][2] = (current_results[i][2] * current_results[0][2])/max_value
        return current_results


    def recommend(self):
        self.scores()
        self.distance_score(user_location)
        self.context()
        results = []
        types_count = {}
        for i in set(PointsOfInterest.instances()):
            if i.hasScore:
                for j in range(len(i.is_a)):
                    if i.is_a[j] not in types_count:
                        types_count[i.is_a[j]] = 0
                        results.append((i.hasName, i.is_a, i.hasScore))
                    else:
                        if types_count[i.is_a[j]] < 3:
                            results.append((i.hasName, i.is_a, i.hasScore))
                            types_count[i.is_a[j]] += 1
                   
        
        results.sort(key = lambda x: x[2], reverse=True)
        results = self.normalize_scores(results)
        self.to_csv(results[0:10])
        return results[0:10]

    def feedback(self,first_results):
        while True:
            rates = input('Do you want to rate some POIs? (y/n) ')
            user_rates = dict()
            if rates not in ['y', 'n']:
                print("Please input \'y' or \'n'")
                continue
            break
            
        if rates.lower() == 'y':
            while True:
                rated_poi = int(input('Choose place to rate (0 to break) '))
                rated_poi = rated_poi - 1
                if rated_poi == -1:
                    break
                if rated_poi not in range(0,10):
                    continue
                
                while True:
                    user_rating = int(input('Rate:  (1 to 5) '))
                    if user_rating not in range(1,6):
                        continue
                    break
                user_rates[rated_poi] = user_rating


            for i in user_rates:
                for j in first_results[i][1]:
                    for k in j.ancestors():
                        if k in self.input_scores:
                            if user_rates[i] in [1,2,3]:
                                self.input_scores[k] = self.input_scores[k] - 1
                                if self.input_scores[k] < 0:
                                    self.input_scores[k] = 0
                            else:
                                self.input_scores[k] = self.input_scores[k] + 1
                                if self.input_scores[k] > 10:
                                    self.input_scores[k] = 10


            new_results = self.recommend()
            self.output(new_results)
            self.feedback(new_results)
        else:
            pass
        
    def run(self):
        self.user_input()
        recommendation_results = self.recommend()
        self.output(recommendation_results)
        self.feedback(recommendation_results)

if __name__ == '__main__':
    scores = Scores(input_scores)
    scores.run()
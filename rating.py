import json

class Ratings:
    ratings = {}

    def deserialize(self):
        with open("ratings.json", "r") as read_file:
            self.ratings = json.load(read_file)

    def serialize(self):
        with open("ratings.json", "w") as write_file:
            json.dump(self.ratings, write_file)

    def get_best(self):
        max = 0
        res = ''
        for src in self.ratings:
            temp = sum(self.ratings[src])/len(self.ratings[src])
            if temp > max:
                max = temp
                res = src
        return res
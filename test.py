import re
import random
searchArtist = "trettmann"
featuresAndProducers = set([])
def validateAndFitness(title):
    #Example valid song: 
    # TRETTMANN FEAT. ALLI NEUMANN - ZEIT STEHT - PROD. KITSCHKRIEG (OFFICIAL VIDEO)
    # TRETTMANN - GRAUER BETON (prod. KITSCHKRIEG) (OFFICIAL VIDEO)
    # Major Lazer & DJ Snake - Lean On (feat. MØ) (Official Music Video)
    # DJ Khaled - BODY IN MOTION (Official Lyric Video) ft. Bryson Tiller, Lil Baby, Roddy Ricch
    #Evaluation
    #   From searchArtist + 10
    #   SearchArtist that is in feature + 7
    #   produced from someone the artist was produced or someone the artist had a feature with +3,


    fitness = 0
    splitted = title.split("-")
    if len(splitted) != 2:
        return fitness
    artists = re.split('feat.|feature| x | & |ft.', splitted[0].lower())
    
    sA = False
    
    names = re.split('feat.|feature|ft.|\(|prod.', splitted[1].lower(), maxsplit=1)
    
    artists = artists + re.split("feat.|feature| x | & |ft.|, |prod.|\(", names[1].lower())
    
    artists = [x for x in artists if "official" not in x]
    
    for count, item in enumerate(artists):
        artists[count] = re.sub('\)|\(', '', artists[count]).strip()
        if artists[count] in featuresAndProducers and not sA:
            fitness = 3
        if artists[count] == searchArtist.lower():
            fitness = 7
            sA = True

    if artists[0] == searchArtist.lower():
        fitness = 10
        sA = True
    
    if sA:
        for item in artists:
            print(item)
            if(item != ""):
                featuresAndProducers.add(item)
    
    print(featuresAndProducers)
    print(artists)
    return fitness


def getTime(label):
    split = label.split("ago") #split[-1] =  1 minute 10 seconds 93,484 views # 10 seconds 93,484 views # 10 minutes 93,434 views
    split = split[-1].split("second") #split = {1 minute 10 , s 93,484 views} # 10, s 93,484 views
    
    if len(split) > 1:
        split =  split[0].split("minute")
        if(len(split) == 1):       # {1 , 10}
            seconds = split[0].strip()
            minutes = 0
        else: 
            split[0] = re.sub('s', '', split[0]).strip() # {1, 10}
            split[1] = re.sub('s', '', split[1]).strip() # {1, 10}
        
            minutes = split[0]
            seconds = split[1]
    else:
        minutes = split[0].split("minute")[0].strip()
        seconds = 0
    
    return int(minutes) * 60 + int(seconds) 

#test = "TRETTMANN FEAT. ALLI NEUMANN - ZEIT STEHT - PROD. KITSCHKRIEG (OFFICIAL VIDEO)"
#print(validateAndFitness(test))
#test = "Major Lazer & DJ Snake - Lean On (feat. MØ) (Official Music Video)"
#print(validateAndFitness(test))
#test = "DJ Khaled - BODY IN MOTION (Official Lyric Video) ft. Bryson Tiller, Lil Baby, Roddy Ricch"
#print(validateAndFitness(test))
#test = "TRETTMANN - GRAUER BETON (prod. KITSCHKRIEG) (OFFICIAL VIDEO)"
#test = "Kitchkrieg - GRAUER BETON (prod. trettmann) (OFFICIAL VIDEO)"
#print(validateAndFitness(test))
test = "1 minute funny videos by MEMES HUB 1 year ago 1 minute 10 seconds 93,484 views"
print(getTime(test))
test = "1  funny videos by MEMES HUB 1 year ago 10 seconds 93,484 views"
print(getTime(test))
test = "1 minute funny videos by MEMES HUB 1 year ago 1 minute 93,484 views"
print(getTime(test))

queue = [[10],[10],[10],[100]]
print([x[0] for x in queue])

print(random.choices(population=range(len(queue)),k=1, weights=[x[0] for x in queue])[0])




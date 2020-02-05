import sys, tweepy, csv
import matplotlib.pyplot as plt
from textblob import TextBlob
import tkinter as tk
from functools import partial


def percentage(part, whole):
    temp = 100 * float(part) / float(whole)
    return (format(temp, '.2f'))

def call_readcsvP():
    with open('resultP.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter='\n')
        for row in csv_reader:
            print("\n".join(row))
    print("\n")

def call_readcsvNeg():
    with open('resultNeg.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter='\n')
        for row in csv_reader:
            print("\n".join(row))
    print("\n")

def call_readcsvN():
    with open('resultN.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter='\n')
        for row in csv_reader:
            print("\n".join(row))
    print("\n")


def call_result(n1, n2):
    topic = str(n1.get())
    NoOfTerms = int(n2.get())

    consumerKey = 'XXXXXX'
    consumerSecret = 'XXXXXXXXX'
    accessToken = 'XXXXXXXXXXXXXX'
    accessTokenSecret = 'XXXXXXXXXXXXXXXXX'

    auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
    auth.set_access_token(accessToken, accessTokenSecret)
    api = tweepy.API(auth)

    tweets = tweepy.Cursor(api.search, q=topic, lang="en").items(NoOfTerms)

    positive = 0
    negative = 0
    neutral = 0
    polarity = 0

    csvP = open('resultP.csv', 'w')
    csvNeg = open('resultNeg.csv', 'w')
    csvN = open('resultN.csv', 'w')
    columnTitleRowP = "Positive_Tweets\n"
    columnTitleRowN = "Neutral_Tweets\n"
    columnTitleRowNeg = "Negative_Tweets\n"
    csvP.write(columnTitleRowP)
    csvNeg.write(columnTitleRowNeg)
    csvN.write(columnTitleRowN)

    positive = 0
    wpositive = 0
    spositive = 0
    negative = 0
    wnegative = 0
    snegative = 0
    neutral = 0

    for tweet in tweets:
        Tweet = str((tweet.text).encode('utf-8'))
        analysis = TextBlob(tweet.text)
        Polar = analysis.sentiment.polarity
        if (Polar == 0):
            row = Tweet + "\n"
            csvN.write(row)
        elif (Polar > 0):
            row = Tweet + "\n"
            csvP.write(row)
        else:
            row = Tweet + "\n"
            csvNeg.write(row)
        if (analysis.sentiment.polarity == 0):
            neutral += 1
        elif (analysis.sentiment.polarity > 0 and analysis.sentiment.polarity <= 0.3):
            wpositive += 1
        elif (analysis.sentiment.polarity > 0.3 and analysis.sentiment.polarity <= 0.6):
            positive += 1
        elif (analysis.sentiment.polarity > 0.6 and analysis.sentiment.polarity <= 1):
            spositive += 1
        elif (analysis.sentiment.polarity > -0.3 and analysis.sentiment.polarity < 0):
            wnegative += 1
        elif (analysis.sentiment.polarity > -0.6 and analysis.sentiment.polarity <= -0.3):
            negative += 1
        elif (analysis.sentiment.polarity > -1 and analysis.sentiment.polarity <= -0.6):
            snegative += 1

    csvP.close()
    csvNeg.close()
    csvN.close()

    positive = percentage(positive, NoOfTerms)
    wpositive = percentage(wpositive, NoOfTerms)
    spositive = percentage(spositive, NoOfTerms)
    negative = percentage(negative, NoOfTerms)
    wnegative = percentage(wnegative, NoOfTerms)
    snegative = percentage(snegative, NoOfTerms)
    neutral = percentage(neutral, NoOfTerms)

    labels = ['Positive [' + str(positive) + '%]', 'Weakly Positive [' + str(wpositive) + '%]',
              'Strongly Positive [' + str(spositive) + '%]', 'Neutral [' + str(neutral) + '%]',
              'Negative [' + str(negative) + '%]', 'Weakly Negative [' + str(wnegative) + '%]',
              'Strongly Negative [' + str(snegative) + '%]']
    sizes = [positive, wpositive, spositive, neutral, negative, wnegative, snegative]
    color = ['yellowgreen', 'lightgreen', 'darkgreen', 'gold', 'red', 'lightsalmon', 'darkred']
    patches, texts = plt.pie(sizes, colors=color, startangle=90)
    plt.legend(patches, labels, loc="best")
    plt.title('Sentimental Analysis on ' + topic + ' by analyzing ' + str(NoOfTerms) + ' Tweets.')
    plt.axis('equal')
    plt.tight_layout()
    plt.show()

    print('Workdone properly')


root = tk.Tk()
root.title('Sentimental Analysis Project')

number1 = tk.StringVar()
number2 = tk.StringVar()

labelTitle = tk.Label(root, text=" Twitter Analysis").grid(row=0, column=1)
labelNum1 = tk.Label(root, text="Enter Keyword/Tag to search about:").grid(row=1, column=0)
labelNum2 = tk.Label(root, text="Enter how many tweets to search:").grid(row=2, column=0)

entryNum1 = tk.Entry(root, textvariable=number1,width="21").grid(row=1, column=1)
entryNum2 = tk.Entry(root, textvariable=number2,width="21").grid(row=2, column=1)
call_result = partial(call_result, number1, number2)
buttonCal = tk.Button(root, text="Click Me to see the piechart", command=call_result,width="21").grid(row=3, column=1,pady=10)

button1 = tk.Button(root, text="Positive Tweets", command=call_readcsvP,width="21").grid(row=5, column=0,padx=15)
button2 = tk.Button(root, text="Negative Tweets", command=call_readcsvNeg,width="21").grid(row=5, column=1,pady=45)
button3 = tk.Button(root, text="Neutral Tweets", command=call_readcsvN,width="21").grid(row=5, column=2,padx=15)
root.mainloop()





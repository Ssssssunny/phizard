# -*-coding:utf-8-*-
# DEPRECATED

import time

from phizard.models.analysis import analyze
from phizard.utils.restful_cli import send_to_server


def statistics(employ_id, start_time=None, end_time=None):
    if start_time or end_time:
        params = {"employ_id":employ_id, "timeline":{"start": start_time,"end": end_time}}
    else:
        params = {"employ_id": employ_id}
    result = send_to_server('POST','/personal_pattern',params)
    if result['code'] == 1:
        content = result['content']
        anger_scores = []
        contempt_scores = []
        disgust_scores = []
        fear_scores = []
        happiness_scores = []
        neutral_scores = []
        sadness_scores = []
        surprise_scores = []

        list = sorted(content.keys())

        for key in list:
            # print key
            c= content[key]
            anger_score = 0
            contempt_score = 0
            disgust_score = 0
            fear_score = 0
            happiness_score = 0
            neutral_score = 0
            sadness_score = 0
            surprise_score = 0

            for i in c:
                anger_score += i['anger']
                contempt_score += i['contempt']
                disgust_score += i['disgust']
                fear_score += i['fear']
                happiness_score += i['happiness']
                neutral_score += i['neutral']
                sadness_score += i['sadness']
                surprise_score += i['surprise']

            amount = len(c)
            # print 'amount:',amount
            anger_score /= amount
            contempt_score /= amount
            disgust_score /= amount
            fear_score /= amount
            happiness_score /= amount
            neutral_score /= amount
            sadness_score /= amount
            surprise_score /= amount
            sum = anger_score + contempt_score + disgust_score + fear_score + happiness_score + neutral_score + sadness_score + surprise_score
            anger_score /= sum
            contempt_score /= sum
            disgust_score /= sum
            fear_score /= sum
            happiness_score /= sum
            neutral_score /= sum
            sadness_score /= sum
            surprise_score /= sum

            # print anger_score+contempt_score+disgust_score+fear_score+happiness_score+neutral_score+sadness_score+surprise_score

            anger_scores.append(anger_score)
            contempt_scores.append(contempt_score)
            disgust_scores.append(disgust_score)
            fear_scores.append(fear_score)
            happiness_scores.append(happiness_score)
            neutral_scores.append(neutral_score)
            sadness_scores.append(sadness_score)
            surprise_scores.append(surprise_score)

        res = analyze({'anger': anger_scores, 'contempt': contempt_scores, 'disgust': disgust_scores, 'fear': fear_scores,
                 'happiness': happiness_scores, 'neutral': neutral_scores, 'sadness': sadness_scores,
                 'surprise': surprise_scores})

        res['date'] = list
        res['graph'] = {'anger': anger_scores, 'contempt': contempt_scores, 'disgust': disgust_scores, 'fear': fear_scores,
                 'happiness': happiness_scores, 'neutral': neutral_scores, 'sadness': sadness_scores,
                 'surprise': surprise_scores}
        return res


if __name__=='__main__':
    start_time = time.strftime('%Y-%m-%d:%H:%M:%S', time.localtime(time.time()-3600*24*30*3))
    end_time = time.strftime('%Y-%m-%d:%H:%M:%S', time.localtime(time.time()))
    statistics(4)

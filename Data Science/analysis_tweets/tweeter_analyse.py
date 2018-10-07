"""
The analysis of tweets from tweeter.com
Done tasks:
-> Data processing
-> Frequency analysis
-> Tweet evaluation rules
-> Most common adjectives
-> Tweets in some period

Useful actions:
frequency -> Frequency analysis
estimations -> Tweet evaluation rules
top of adjectives -> Most common adjectives
hours -> Tweets in some period

Work done by Mihail Krupin
"""
import re
import pymorphy2
import matplotlib.pyplot as plt


def modify_tweets(file):
    """
    Modifies our tweets: delete hashtags, links,
    symbols of punctuations
    and some unuseful words

    :param file:
    :return dict with modified tweets:
    """
    with open(file, encoding='utf-8') as f_obj:
        tweets = f_obj.read().split('**********')

        tweeter_data = {}

        count = 0
        for tweet in tweets:
            tweet = re.sub(r'#\w+', '', tweet)
            check_date = re.findall(r'\d{2}:\d{2}', tweet)
            check_text = re.findall(r'\n\D+', tweet)

            if not check_text:
                tweets.pop(tweets.index(tweet))
            if check_text:
                check_date[0] = check_date[0] + str(count)
                count += 1
                tweeter_data[check_date[0]] = check_text[0].strip()

        morph = pymorphy2.MorphAnalyzer()
        for key, val in tweeter_data.items():
            val = re.sub(r'\n', ' ', val)
            val = re.sub(r'[«»a-zA-Z./\'":!?,()@–-]', '', val)
            val = val.split()
            for word in val:
                check_pos = morph.parse(word.lower())[0].tag.POS
                normal_form = morph.parse(word.lower())[0].normal_form

                if '…' in word:
                    val[val.index(word)] = ''
                    continue

                if check_pos == 'PREP' or check_pos == 'PRCL' or \
                   check_pos == 'CONJ' or check_pos == 'ADVB':
                    val[val.index(word)] = ''
                else:
                    val[val.index(word)] = normal_form
            val = ' '.join(val)
            tweeter_data[key] = val
        return tweeter_data


def frequency(data):
    """
    Consider how many times every word occurs
    in our file

    :param data:
    :return the tuple (word, quantity):
    """
    info = {}
    for tweet in data.values():
        for word in tweet.split():
            word = word.lower()
            if word not in info.keys():
                info[word] = 1
            if word in info.keys():
                info[word] += 1

    info = sorted(info.items(), key=lambda x: x[1], reverse=True)
    save_frequency(info)
    return info


def save_frequency(tuple_tweets):
    """
    Save our the result of frequency function
    in file

    :param tuple_tweets:
    :return:
    """
    count_words = len(tuple_tweets)
    with open(r'frequency.txt', 'w') as f_obj:
        for i in tuple_tweets:
            f_obj.write(i[0] + '-' + str(i[1]) + '-' +
                        str(round(int(i[1])*100/count_words, 2)) + '%\n')


def count_tonality(tweet_list):
    """
    Consider the number of pos, net and neg tweets

    :param tweet_list:
    :return the list with pos, net and neg tweets:
    """
    with open(r'estimations.txt') as file:
        emp_marks = {line.split(':')[0].strip(): line.split(':')[1].strip() for line in file}

    pos_marks = []
    net_marks = []
    neg_marks = []
    for i in tweet_list:
        if i in emp_marks.keys():
                if emp_marks[i] == '1':
                    pos_marks.append(i)
                if emp_marks[i] == '0':
                    net_marks.append(i)
                if emp_marks[i] == '-1':
                    neg_marks.append(i)

    sum_words = len(pos_marks) + len(net_marks) + len(neg_marks)

    return sum_words


def estimations(data):
    """
    Define some rules and with their help
    define tweet semantic
    Then draw the graph

    :param data:
    :return:
    """
    with open(r'estimations.txt') as file:
        emp_marks = {line.split(':')[0].strip(): line.split(':')[1].strip() for line in file}

    num_tweets = len(data)

    # First rule
    first_rule = []
    for tweet in data.values():
        count = 0
        tweet = tweet.split()
        for word in tweet:
            if word in emp_marks.keys():
                count += int(emp_marks[word])
                if tweet.index(word) == len(tweet) - 1:
                    first_rule.append(count)

    neg_first = len([i for i in first_rule if i < 0])
    pos_first = len([i for i in first_rule if i > 0])
    net_first = len([i for i in first_rule if i == 0])
    for_first_rule = [pos_first, neg_first, net_first]

    # Second rule
    # if % > 0.5 - pos, % < 0.05 - neg
    second_rule = []
    for tweet in data.values():
        count = 0
        tweet = tweet.split()
        for word in tweet:
            if word in emp_marks.keys():
                count += int(emp_marks[word])
                if tweet.index(word) == len(tweet) - 1:
                    second_rule.append(count)

    neg_sec = len([x for x in second_rule if abs(x) / 100 < 0.05])
    pos_sec = len([x for x in second_rule if abs(x) / 100 > 0.05])
    net_sec = len([x for x in second_rule if abs(x) / 100 == 0.05])
    for_second_rule = [pos_sec, neg_sec, net_sec]

    f_obj = open(r'classifications.txt', 'w')
    f_obj.write('The sum rule\n')
    f_obj.close()
    save_classification(for_first_rule)
    f_obj = open(r'classifications.txt', 'a')
    f_obj.write('The fraction rule\n')
    f_obj.close()
    save_classification(for_second_rule)

    width = 0.95

    plt.bar(range(1, 2), [pos_first/num_tweets], width=width, color='red')
    plt.bar(range(2, 3), [net_first/num_tweets], width=width, color='blue')
    plt.bar(range(3, 4), [neg_first/num_tweets], width=width, color='green')
    plt.bar(range(5, 6), [pos_sec/num_tweets], width=width, color='red')
    plt.bar(range(6, 7), [net_sec/num_tweets], width=width, color='blue')
    plt.bar(range(7, 8), [neg_sec/num_tweets], width=width, color='green')

    plt.ylabel('percents')
    plt.xticks([2, 6], ['The sum rule', 'The fraction rule'])
    plt.show()


def save_classification(list_rule):
    """
    Save results of estimations function to the file

    :param list_rule:
    :return:
    """
    num_tweets = 97
    with open(r'classifications.txt', 'a') as f_obj:
        f_obj.write('Positive - {0} - {1}%\n'.format(list_rule[0],
                                                     round(list_rule[0] * 100 / num_tweets), 4))
        f_obj.write('Negative - {0} - {1}%\n'.format(list_rule[1],
                                                     round(list_rule[1] * 100 / num_tweets), 4))
        f_obj.write('Neutral - {0} - {1}%\n'.format(list_rule[2],
                                                    round(list_rule[2] * 100 / num_tweets), 4))
        f_obj.write('\n')


def top_adjectives(data):
    """
    Find top-5 the most common adjectives
    Then draw the graph

    :param data:
    :return:
    """
    with open(r'estimations.txt') as f_obj:
        emp_marks = {line.split(':')[0].strip(): line.split(':')[1].strip() for line in f_obj}

    morph = pymorphy2.MorphAnalyzer()

    info = data

    new_info = {}
    for i in info:
        check_pos = morph.parse(i[0])[0].tag.POS
        if check_pos == 'ADJF':
            new_info.update([i])

    pos_adj = []
    neg_adj = []
    for i in new_info.keys():
        if i in emp_marks.keys():
            if emp_marks[i] == '1':
                pos_adj.append((i, new_info[i]))
            if emp_marks[i] == '-1':
                neg_adj.append((i, new_info[i]))

    f_obj = open(r'adjectives.txt', 'w')
    f_obj.write('Top-5 positive adjectives:\n')
    f_obj.close()
    save_adj(pos_adj)
    f_obj = open(r'adjectives.txt', 'a')
    f_obj.write('Top-5 negative adjectives:\n')
    f_obj.close()
    save_adj(neg_adj)

    width = 0.95
    plt.bar(range(1, 6), list(map(lambda x: x[1]*100/len(pos_adj), pos_adj[:5])), width=width)
    plt.bar(range(7, 12), list(map(lambda x: x[1]*100/len(neg_adj), neg_adj[:5])), width=width)

    plt.ylabel('percents')
    plt.xticks([3, 9], ['Top-5 positive', 'Top-5 negative'])
    plt.show()


def save_adj(list_adj):
    """
    Save the result of part_speech function to the file

    :param list_adj:
    :return:
    """
    with open(r'adjectives.txt', 'a') as f_obj:
        for i in list_adj[:5]:
            f_obj.write(i[0] + ' - ' + str(i[1]) + ' - ' +
                        str(round(i[1]*100/len(list_adj), 2)) + '%\n')
        f_obj.write('\n')


def tonality_tweets_in_period(dict_tweets):
    """
    Count pos, net and neg tweets in some period
    Then draw the graph

    :param dict_tweets:
    :return:
    """
    count_hour = 20
    pos_est = 0
    net_est = 0
    neg_est = 0
    all_time_marks = []
    for time in dict_tweets.keys():
        hours_t = int(time.split(':')[0])
        if hours_t != count_hour:
            all_marks = [pos_est, net_est, neg_est]
            if hours_t == 19:
                f_obj = open(r'hours.txt', 'w')
                f_obj.write('Tweets in periods:\n')
                f_obj.close()
            save_tweets_in_period(count_hour, all_marks)
            all_time_marks.append([pos_est, neg_est, neg_est])
            all_marks.clear()
            pos_est = 0
            net_est = 0
            neg_est = 0
            count_hour -= 1

        if hours_t == count_hour:
            list_tweet = dict_tweets[time].split()
            mark_tweet = count_tonality(list_tweet)    # возвращает сумму оценки всех слов
            if mark_tweet > 0:
                pos_est += 1
            if mark_tweet == 0:
                net_est += 1
            if mark_tweet < 0:
                neg_est += 1

        if time == list(dict_tweets.keys())[-1]:    # определяем последний элемент в словаре
            all_marks = [pos_est, net_est, neg_est]
            save_tweets_in_period(hours_t, all_marks)
            all_time_marks.append([pos_est, net_est, neg_est])

    width = 0.97
    plt.bar(range(1, 4), all_time_marks[0], width=width)
    plt.bar(range(4, 7), all_time_marks[1], width=width)
    plt.bar(range(7, 10), all_time_marks[2], width=width)
    plt.bar(range(10, 13), all_time_marks[3], width=width)
    plt.bar(range(13, 16), all_time_marks[4], width=width)

    plt.annotate('20-21', xy=(1, 6), xytext=(0.5, 15),
                 arrowprops=dict(facecolor='black', shrink=0.05))
    plt.annotate('19-20', xy=(4, 10), xytext=(3.5, 19),
                 arrowprops=dict(facecolor='black', shrink=0.05))
    plt.annotate('18-19', xy=(7, 24), xytext=(6.5, 34),
                 arrowprops=dict(facecolor='black', shrink=0.05))
    plt.annotate('17-18', xy=(9.5, 48), xytext=(6.5, 48),
                 arrowprops=dict(facecolor='black', shrink=0.05))
    plt.annotate('16-17', xy=(13.5, 55), xytext=(14.5, 55),
                 arrowprops=dict(facecolor='black', shrink=0.05))
    plt.xlabel('Periods where tweets were the most positive')
    plt.show()


def save_tweets_in_period(hours_f, num_list):
    """
    Save the result of hours function to the file

    :param hours_f:
    :param num_list:
    :return:
    """
    with open(r'hours.txt', 'a') as f_obj:
        f_obj.writelines(str(hours_f) + ' - ' + str(hours_f+1) + ' - ' +
                         '{0}/{1}/{2}'.format(num_list[0], num_list[1], num_list[2]) + '\n')


def main():
    """
    The main function where all function are started

    :return:
    """
    tweets_file = r'tweets.txt'
    print('Hello, fellow! I know u want some analysis:)')
    while True:
        action = input('What do you want to see?')
        if action == 'frequency':
            frequency(modify_tweets(tweets_file))
            print('Information in \'frequency.txt\' file')
        if action == 'estimations':
            estimations(modify_tweets(tweets_file))
            print('Information in \'classifications.txt\' file')
        if action == 'top of adjectives':
            top_adjectives(frequency(modify_tweets(tweets_file)))
            print('Information in \'adjectives.txt\' file')
        if action == 'hours':
            tonality_tweets_in_period(modify_tweets(tweets_file))
            print('Information in \'hours.txt\' file')
        if action == 'exit':
            print('See you later!')
            break


if __name__ == '__main__':
    main()

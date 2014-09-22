import csv
from collections import namedtuple
import os
import operator
from math import ceil

PROGRAM_PATH = os.path.realpath(os.path.dirname(__file__))
CSV_PATH = os.path.join(PROGRAM_PATH, 'data/presenters.csv')

NUM_SESSIONS = 3

def read_csv():
    with open(CSV_PATH) as csv_file:
        csv_reader = csv.reader(csv_file)
        csv_reader.next()
        sortedlist = sorted(csv_reader,
            key=operator.itemgetter(1),
            reverse=True)  # sorted by descending number of hours
        return sortedlist


def divide_presentation_hours(num_hours):
    total_num_hours = num_hours
    time_per_session = ceil(float(num_hours) / float(NUM_SESSIONS))
    session_list = []
    for session in range(0, NUM_SESSIONS):
        session_length = time_per_session
        if num_hours - session_length == 0:
            session_length = time_per_session - 1
        if session < NUM_SESSIONS - 1:
            if session_length > total_num_hours / 2:
                session_length = session_length - 1
        else:
            session_length = num_hours
        num_hours = num_hours - session_length
        session_list.append(session_length)
    return session_list


def create_session_dict(total_hours, session_list, sorted_list):
    session_dict = {}
    return_msg = ""
    for index, value in enumerate(session_list):
        session_dict["session%s" % index] = {"hours": value,
                                             "presenters": []}

    while total_hours > 0:
        for index, session in enumerate(session_list):
            if session != 0 and len(sorted_list) > 0:
                presenter = sorted_list.pop()
                if session - int(presenter[1]) >= 0:
                    session_list[index] = session - int(presenter[1])
                    key_str = "session%s" % index
                    session_dict[key_str]["presenters"].append(presenter)
                else:
                    sorted_list.append(presenter)
                total_hours = total_hours - int(presenter[1])
            else:
                total_hours = 0
                if len(sorted_list) <= 0:
                    return_msg = "Not enough presenters"
                    break
    return session_dict, return_msg

if __name__ == "__main__":
    total_hours = 35
    session_list = divide_presentation_hours(total_hours)
    print "Session wise distribution of hours for %s Total hours" % total_hours
    print "Total %s sessions: \nsession0: %s hours \n"\
            "session1: %s hours and \nsession2: %s hours" % (NUM_SESSIONS,
                                                            session_list[0],
                                                            session_list[1],
                                                            session_list[2],)
    sorted_list = read_csv()

    session_dict, return_msg = create_session_dict(total_hours, session_list, sorted_list)
    print session_dict
    print return_msg




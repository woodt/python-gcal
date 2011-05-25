#!/usr/bin/env python

import iso8601
from optparse import OptionParser
import gdata.calendar.service

def query(calendar, options):
    cal = gdata.calendar.service.CalendarService()
    query = gdata.calendar.service.CalendarEventQuery(calendar, 'public', 'composite')
    if options.start_date:
        query.start_min = options.start_date
    if options.end_date:
        query.start_max = options.end_date
    query.singleevents = 'true'
    feed = cal.CalendarQuery(query)
    hours = dict()
    for entry in feed.entry:
        for when in sorted(entry.when, key=lambda w: w.start_time):
            start_time = iso8601.parse_date(when.start_time)
            start_date = start_time.date()
            end_time = iso8601.parse_date(when.end_time)
            hours[start_date] = (entry.title.text, start_time, end_time)

    for date, (title, start_time, end_time) in sorted(hours.items()):
        start_time = start_time.time()
        end_time = end_time.time()
        print "%s | %s to %s | %s" % (date, start_time, end_time, title)

def main():
    parser = OptionParser()
    parser.add_option("-s", "--start", dest="start_date")
    parser.add_option("-e", "--end", dest="end_date")

    (options, args) = parser.parse_args()

    if len(args) == 1:
        url = args[0]
        query(url, options)
                      
if __name__ == '__main__':
    main()

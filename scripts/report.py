#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argh

#import pprint
from dateutil import parser

from targetlib.togglapi import TogglReportsAPI
from togglcli import settings
from togglcli.helpers import ms_to_hr, default_workspace_id


api = TogglReportsAPI(settings.API_TOKEN, settings.TIMEZONE)


@argh.arg('workspace-id', help='workspace id', nargs='?', default=None)
def weekly(workspace_id):
    workspace_id = default_workspace_id(workspace_id)
    data = api.get_weekly(workspace_id)
    #pprint.pprint(data)

    for d in data['data']:
        print d['title']['client'], d['title']['project']
        print u"last 7:", [ms_to_hr(ms) for ms in d['totals'][:-1]]
        print u"total:", ms_to_hr(d['totals'][-1])


@argh.arg('workspace-id', help='workspace id', nargs='?', default=None)
def details(workspace_id):
    workspace_id = default_workspace_id(workspace_id)
    data = api.get_details(workspace_id)
    #pprint.pprint(data)

    day = ""
    project = ""
    for d in data['data']:
        this_project = "{} {}".format(d['client'], d['project'])
        if project != this_project:
            project = this_project
            print project
        this_day = parser.parse(d['start']).date().isoformat()
        if day != this_day:
            day = this_day
            print day
        print u"- {} ({})".format(d['description'], ms_to_hr(d['dur']))


@argh.arg('workspace-id', help='workspace id', nargs='?', default=None)
def summary(workspace_id):
    workspace_id = default_workspace_id(workspace_id)
    data = api.get_summary(workspace_id)
    #pprint.pprint(data)

    for d in data['data']:
        print u"{} {} ({})".format(
            d['title']['client'],
            d['title']['project'],
            ms_to_hr(d['time']))
        for i in d['items']:
            print u"- {} ({})".format(i['title']['time_entry'], ms_to_hr(i['time']))


argh_parser = argh.ArghParser()
argh_parser.add_commands([weekly, details, summary])

if __name__ == '__main__':
    argh_parser.dispatch()

# -*- coding: utf-8 -*-
from __future__ import print_function
import pickle
import re
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

## added to script
import os
import requests
import json
import sys
import datetime
import calendar
from dateutil.relativedelta import relativedelta
import codecs


# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']

def drivedata():
    print('Trying to get Google Drive date.')
    #Shows basic usage of the Drive v3 API.
    #    Prints the names and ids of the first 10 files the user has access to.

    creds = None
    lesson = {}
    informationlist1 = []
    informationlist2 = []
    formated = ''
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('drive', 'v3', credentials=creds)

    # Call the Drive v3 API
    results = service.files().list(
        pageSize=100, fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])
    loop = 0
    if not items:
        print('No files found.')
    else:
        for item in items:
            lessonlist1 = {}
            lessonlist2 = {}
            if '4828855803' not in u'{0}'.format(item['name']):
                continue
            else:
                lessonlist1['date'] = u'{0}'.format(item['name'])[0:10]
                lessonlist1['time'] = u'{0}'.format(item['name'])[11:19]
                lessonlist1['teacher'] = u'{0}'.format(item['name'])[20:33]
                lessonlist1['id'] = [u'{0}'.format(item['id'])]

                lessonlist2['date'] = u'{0}'.format(item['name'])[0:10]
                lessonlist2['time'] = u'{0}'.format(item['name'])[11:19]
            informationlist1.append(lessonlist1)
            informationlist2.append(lessonlist2)
    return informationlist1,informationlist2

def localdata():
    print('Starting parse local date.')
    #value for using later on
    posts = {}
    informationlist = []
    data = os.system('ls -Art ../_posts/ | tail -n 1 > info.txt')
    info = open("info.txt", "r")
    allinfo = info.readlines()
    for line in allinfo:
        posts = {}
        posts['date'] = line[0:10]
        posts['time'] = line[11:15]
        informationlist.append(posts)
    return informationlist

def findNewFiles(lastpost, list1):
    print('Search for new data.')
    newFilesList = []
    type(lastpost[0]['date'])
    list1.sort()
    for item1 in list1:
        if item1['date'] > lastpost[0]['date']:
            newFilesList.append({'date':item1['date'],'time':item1['time']})
    return newFilesList

def addKey(list1):
    print('Add key info.')
    list2 = []
    key = 0
    for item1 in list1:
        key += 1
        item1['key'] = key
        list2.append(item1)
    return list2

def addID(list1,driveWithID):
    print('Add ID info.')
    list2 = []
    for item1 in list1:
        for item2 in driveWithID:
            if item1['date'] == item2['date'] and item1['time'] == item2['time']:
                list2.append({'key':item1['key'],'date':item1['date'],'time':item1['time'],'id':item2['id']})
    return list2

def marginFiles(list1):
    print("Start margin the files.")
    newIDs = []
    newDict = {}
    previousItem = list1[0]
    list2 = [previousItem]
    for item1 in list1[1:]:
        if item1['date'] == previousItem['date']:
            if int(item1['time'][0:2]) <= int(previousItem['time'][0:2])+2:
                #margin ID's
                for loop in range(len(previousItem['id'])):
                    newIDs.append(previousItem['id'][loop])
                newIDs.append(item1['id'][0])

                newDict = {'date':previousItem['date'],'id':newIDs,'key':previousItem['key'],'time':previousItem['time']}
                index = next((index for (index, d) in enumerate(list2) if d['key'] == newDict['key']), None)
                list2[index] = newDict
                previousItem = item1
                newIDs = []
            else:
                previousItem = item1
                list2.append(item1)
        else:
            previousItem = item1
            list2.append(item1)
    return list2

def addHebDate(list1):
    print('Get hebrew date.')
    hebday = [u'יום שני',u'יום שלישי',u'יום רביעי',u'יום חמישי',u'יום שישי',u'יום שבת',u'יום ראשון']
    #get hebrew date
    for item1 in list1:
        year = item1['date'][0:4]
        month = item1['date'][5:7]
        day = item1['date'][8:10]
        jsonInfo = requests.get('https://www.hebcal.com/converter/?v=1&cfg=json&gd=' +
        day + '&gm=' + month + '&gy=' + year + '&h=on').json()
        item1['hebdate'] = jsonInfo['hebrew']
        item1['hebday'] = hebday[datetime.datetime(int(year),int(month),int(day)).weekday()]
    return list1

def addHebInfo(list1):
    print('Get hebrew information')
    rangeDate = []
    apiInfo = []
    oldestDate = datetime.date(int(list1[0]['date'][0:4]), int(list1[0]['date'][5:7]), int(list1[0]['date'][8:10]))
    newestDate = datetime.date(int(list1[-1]['date'][0:4]), int(list1[-1]['date'][5:7]), int(list1[-1]['date'][8:10]))
    while oldestDate <= newestDate + relativedelta(months=1):
        rangeDate.append(oldestDate)
        oldestDate += relativedelta(months=1)
    print(rangeDate)
    for date in rangeDate:
        dateRequest = [str(date)[0:4],str(date)[5:7]]
        jsonInfo = requests.get('https://www.hebcal.com/hebcal/?v=1&cfg=json' +
        ';year='+ dateRequest[0] + ';month=' + dateRequest[1] + ';c=on;geo=geoname;city=IL-Jerusalem' +
        ';m=0;s=on;maj=on;min=on;mod=on;nx=on;mf=on').json()[u'items']
        for item1 in jsonInfo:
            if item1[u'category'] == u'parashat' or item1[u'category'] == u'holiday':
                apiInfo.append(item1)
    for item1 in list1:
        for item2 in apiInfo:
            if item2[u'category'] == u'holiday':
                if item1['date'] == item2[u'date']:
                    item1['holiday'] = item2[u'hebrew']
                    print('item1 date:',item1['date'],'item holiday:',item1['holiday'])
                    continue
            if item2[u'category'] == u'parashat':
                print('compar dates:',item1['date'],item2[u'date'])
                if item1['date'] <= item2[u'date']:
                    item1['parasha'] = item2[u'hebrew']
                    print('item1 date:',type(item1['date']),'item parasha:',type(item1['parasha']))
                    break
    return list1

def addDayPeriod(list1):
    print('Adding day period information')
    for item1 in list1:
        if item1['time'] < '07.30.00':
            item1['period'] = u'שיעור בוקר'
        elif item1['time'] < '12.30.00':
            item1['period'] = u'שיעור בוקר'
        elif item1['time'] < '16.30.00':
            item1['period'] = u'שיעור צהריים'
        elif item1['time'] < '20.30.00':
            item1['period'] = u'שיעור אחר הצהריים'
        elif item1['time'] < '22.00.00':
            item1['period'] = u'שיעור ערב'
    for item1 in list1:
        print('<------Info------->')
        print('this is item1 date:',item1['key'],item1['date'],item1['time'],item1['period'])
        print('this is item1 info:',item1['hebday'],item1['hebdate'],item1['parasha'],item1['id'])
    return list1


def createPosts(list1):
    for item1 in list1:
        postName = '../_posts/' + item1['date'] + '-' + item1['time'] + '.html'
        post = codecs.open(postName, 'w', encoding="utf-8")
        s = ' '
        htmlinfo = ''
        post.write('---' +'\n')
        post.write('layout: post'+'\n')
        post.write('title:' +s+ item1['hebday'] +s+ item1['hebdate'] +s+ item1['period']+s+item1['parasha']+'\n')
        post.write('subtitle: ' + u'שיעור בזוהר הקדוש'+'\n')
        post.write('date:' +s+ item1['date'] +s+ item1['time'][0:2] +':' + item1['time'][3:5] + ':' + item1['time'][6:8]+'\n')
        post.write('background: "/img/bg-post.jpg"'+'\n')
        post.write('tags: '+'[')
        if 'holiday' in item1:
            post.write(item1['holiday']+',')
            post.write(item1['period']+',')
            post.write(item1['parasha']+',')
        else:
            post.write(item1['period']+',')
            post.write(item1['parasha']+',')
        ## add tags of leasessn location
        if item1['hebday'] == u'יום שני' and item1['period'] == u'שיעור ערב':
            post.write(u'שיעורים ברעננה'+',')
        elif item1['hebday'] == u'יום רביעי' and item1['period'] == u'שיעור ערב':
            post.write(u'שיעורים בבני ברק'+',')
        elif item1['hebday'] == u'יום שישי' and item1['time'] >= '09.00.00':
            post.write(u'שיעורים בגבעת שמואל'+',')
        post.write(']\n---'+'\n')

        for id in item1['id']:
            htmlinfo+= '<div class="imgbox">\n'
            htmlinfo+= '<audio class="audiobar" controls="controls" style="width: 100%;">\n'
            htmlinfo+= '<source src="https://docs.google.com/uc?export=download&id=' + id + '">\n'
            htmlinfo+= '</audio>\n<br>\n'
        post.write(htmlinfo)
        post.close()
        




if __name__ == '__main__':
    driveWithID,driveWithoutID = drivedata()
    localinformation = localdata()
    newFilesList = findNewFiles(localinformation,driveWithoutID)
    newFilesList = addKey(newFilesList)
    newFilesList = addID(newFilesList,driveWithID)
    newFilesList = marginFiles(newFilesList)
    newFilesList = addHebDate(newFilesList)
    newFilesList = addHebInfo(newFilesList)
    newFilesList = addDayPeriod(newFilesList)
    createPosts(newFilesList)

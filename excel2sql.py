# encoding: utf8
import pandas as pd
from app import db, Event, Page, AppVersion

df = pd.read_excel('分页面打点纪录点.xlsx', sheetname=['4.6', '4.7', '4.8', '4.9', '4.10'])
for sheet in df:
    df[sheet] = df[sheet].fillna('')
    appversion = AppVersion(sheet)
    db.session.add(appversion)
    db.session.commit()
    page_id = {}
    for i in df[sheet].index:
        row = df[sheet].ix[i]
        if row[u'页面'] == '':
            continue
        if i == 0:
            page_web = Page(appversion.id, row[u'页面'], row['page_key'], 'web')
            db.session.add(page_web)
            page_ios = Page(appversion.id, row[u'页面'], row['page_key'], 'ios')
            db.session.add(page_ios)
            page_and = Page(appversion.id, row[u'页面'], row['page_key'], 'andriod')
            db.session.add(page_and)
            db.session.commit()
            page_id[row[u'页面'] + 'web'] = page_web.id
            page_id[row[u'页面'] + 'ios'] = page_ios.id
            page_id[row[u'页面'] + 'and'] = page_and.id
        elif i > 0 and df[sheet].ix[i-1][u'页面'] != row[u'页面']:
            page_web = Page(appversion.id, row[u'页面'], row['page_key'], 'web')
            db.session.add(page_web)
            page_ios = Page(appversion.id, row[u'页面'], row['page_key'], 'ios')
            db.session.add(page_ios)
            page_and = Page(appversion.id, row[u'页面'], row['page_key'], 'andriod')
            db.session.add(page_and)
            db.session.commit()
            page_id[row[u'页面'] + 'web'] = page_web.id
            page_id[row[u'页面'] + 'ios'] = page_ios.id
            page_id[row[u'页面'] + 'and'] = page_and.id

        if row['se_category.1'] != '' or row['se_action.1'] != '':
            event_ios = Event(row[u'事件'], row[u'对象'], page_id[row[u'页面'] + 'ios'], row['type'], row['sub_type'], row['se_category.1'],
                              row['se_action.1'], row[u'额外信息'])
            db.session.add(event_ios)
        if row['se_category'] != '' or row['se_action'] != '':
            event_and = Event(row[u'事件'], row[u'对象'], page_id[row[u'页面'] + 'and'], row['type'], row['sub_type'], row['se_category'],
                              row['se_action'], row[u'额外信息'])
            db.session.add(event_and)
        if row['se_category.2'] != '' or row['se_action.2'] != '':
            event_web = Event(row[u'事件'], row[u'对象'], page_id[row[u'页面'] + 'web'], row['type'], row['sub_type'], row['se_category.2'],
                              row['se_action.2'], row[u'额外信息'])
            db.session.add(event_web)

db.session.commit()

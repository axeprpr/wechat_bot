#!/usr/bin/python
# -*- coding:UTF-8 -*-
from redminelib import Redmine
import re,sys
reload(sys)
sys.setdefaultencoding('utf8')

REDMINE_URL = 'http://redmine.astute-cloud.com'
USERNAME = 'xv.yayun@astute-tec.com'
PASSWORD = '1'
HELP = "格式错误。\n录单：@frog 录单 项目名（如云计算测试） 主题；\n 查单：@frog 查单 主题；\n 录工时（仅限运维人员）：@frog 录工时 某项目 工时数 信息；\n 查工时：@frog 查工时 某项目"

def project_search(name):
    redmine = Redmine(REDMINE_URL, username=USERNAME, password=PASSWORD)
    for p in redmine.project.all():
        if name in p.name:    
            return p

def issue_add(project_id, subject):
    redmine = Redmine(REDMINE_URL, username=USERNAME, password=PASSWORD)
    new_issue = redmine.issue.new()
    new_issue.project_id = project_id
    new_issue.subject = subject
    new_issue.save()

def issue_search(subject, time_entries=False):
    redmine = Redmine(REDMINE_URL, username=USERNAME, password=PASSWORD)
    issues = []
    for i in redmine.issue.filter(status__name__not__in="关闭"):
        if subject in i.subject:
            if not time_entries:
                issues.append(i)
            else:
                if '工时' in i.subject:
                    issues.append(i)
    return issues

def issue_update(issue_id, notes):
    redmine = Redmine(REDMINE_URL, username=USERNAME, password=PASSWORD)
    redmine.issue.update(issue_id, notes=notes)

def issue_total_spent_hours(issue_id):
    redmine = Redmine(REDMINE_URL, username=USERNAME, password=PASSWORD)
    issue = redmine.issue.get(issue_id)
    return issue.total_spent_hours

def issue_time_entries(issue_id, hours, comments):
    redmine = Redmine(REDMINE_URL, username=USERNAME, password=PASSWORD)
    time_entry = redmine.time_entry.new()
    time_entry.issue_id = issue_id
    time_entry.hours = hours
    time_entry.comments = comments
    time_entry.save()

def redmine_handle(message):
    message_dict = message.split()
    try:
        for i in message_dict:
            if '@' in i:
                message_dict.remove(i)
        if message_dict[0] in ['录单','redmine录单']:
            project = project_search(message_dict[1])
            issue_add(project.id, ''.join(message_dict[2:]))
            return issue_search(''.join(message_dict[2:]))
        elif message_dict[0] in ['查单','redmine查单']:
            return issue_search(message_dict[1])
        elif message_dict[0] in ['查工时','redmine查工时']:
            issue = issue_search(message_dict[1], time_entries=True)[0]
            return  str(issue.subject) + ' #' + str(issue.id) + ' ' + "当前总工时：" + str(issue_total_spent_hours(issue.id))
        elif message_dict[0] in ['录工时','redmine录工时']:
            issue = issue_search(message_dict[1], time_entries=True)[0]
            issue_time_entries(issue.id, float(message_dict[2]), ''.join(message_dict[3:]))
            issue_update(issue.id, ''.join(message_dict[3:]))
            return str(issue.subject) + ' #' + str(issue.id) + ' ' + "当前总工时：" + str(issue_total_spent_hours(issue.id))
        else:
            return HELP
    except:
        return HELP

def main():
#    print redmine_handle('redmine录单 运维 金科院工时单')
    print redmine_handle('redmine查单 金科院')
#    print redmine_handle('redmine录工时 金科院 1 徐亚运 测试用的')
    print redmine_handle('redmine查工时 金科院')

if __name__ == '__main__':
  main()

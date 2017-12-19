import argparse
import datetime
from enum import Enum

import numpy as np
import os
import re
from docxtpl import DocxTemplate


def array_split(arr, chunks):
    result = []
    chunk_len = np.math.ceil(len(arr) / chunks)

    for i in range(chunks):
        result.append(arr[i * chunk_len:i * chunk_len + chunk_len])

    return result


def print_to_stdout(tickets):
    for i, ticket in enumerate(tickets):
        print('Ticket {}'.format(i))
        for j, fq in enumerate(ticket['formal_questions']):
            print(j + 1)
            for q in fq:
                print('{}: {} {}'.format(q['group'], q['title'], q['text']))
            print('-----')
        print('')


def save_to_docx(template_file, output_file, ctx):
    doc = DocxTemplate(template_file)
    
    doc.render(ctx)
    doc.save(output_file)
    

def russian_month(m):
    return {
        1: 'января',
        2: 'февраля',
        3: 'марта',
        4: 'апреля',
        5: 'мая',
        6: 'июня',
        7: 'июля',
        8: 'августа',
        9: 'сентября',
        10: 'октября',
        11: 'ноября',
        12: 'декабря',
    }[m]


def generate(args, questions_file, template_file, output_file):
    groups, group_types = parse_questions(questions_file)
    
    if args.groups is not None:
        use_groups = args.groups.split(',')
        groups = list(filter(lambda g: g['short'] in use_groups, groups))

    if args.groups_count is None:
        args.groups_count = len(groups)

    if args.formal_questions_count is None:
        args.formal_questions_count = args.groups_count

    tickets = []
    for i in range(args.tickets_count):
        selected_groups = []
        ids = np.random.choice(len(groups), args.groups_count, False)
        ids.sort()
        for _id in ids:
            selected_groups.append(groups[_id])

        # collect all questions to one list
        questions = []
        for group in selected_groups:
            questions_in_group = len(group)
            group_questions = group['questions']
            ids = np.random.choice(
                len(group_questions),
                min(questions_in_group,
                    args.questions_per_group),
                False)

            for _id in ids:
                questions.append(group_questions[_id])

        formal_questions = array_split(questions, args.formal_questions_count)
        tickets.append({
            'formal_questions': formal_questions
        })

    # print_to_stdout(tickets)
    ctx = {
        'course_name': args.title,
        'tickets': tickets,
        'date': {
            'day': args.date.day,
            'month': russian_month(args.date.month),
            'year': args.date.year
        },
    }
    save_to_docx(template_file, output_file, ctx)


def parse_questions(questions_file):
    class State(Enum):
        BEGIN = 0
        GROUP_TITLE = 1
        TITLE = 2
        QUESTION = 3
        EMPTY_LINE = 4

    state = State.BEGIN

    groups = []
    group_types = []

    question = {}
    group = {}

    title_regexp = re.compile('\d+\. ')

    def save_question():
        nonlocal question
        question['group'] = group['title']
        group['questions'].append(question)
        question = {}

    def create_question(title):
        if not title.endswith('.'):
            title += '.'
        question['title'] = title_regexp.sub('', title)
        question['text'] = ''

    def save_group():
        nonlocal group
        groups.append(group)
        group_types.append(group['short'])
        group = {}

    def create_group(title):
        short, title = title.split('|')
        group['short'] = short.strip()
        group['title'] = title.strip()
        group['questions'] = []

    with open(questions_file, encoding='utf-8-sig') as f:
        for line in f:
            line = line.strip()

            if state == State.BEGIN:
                create_group(line)
                state = State.GROUP_TITLE
            elif state == State.GROUP_TITLE:
                create_question(line)
                state = State.TITLE
            elif state == State.TITLE:
                if title_regexp.match(line):
                    # new question
                    save_question()
                    create_question(line)
                    state = State.TITLE
                else:
                    question['text'] = line
                    state = State.QUESTION
            elif state == State.QUESTION:
                if len(line) == 0:
                    save_question()
                    state = State.EMPTY_LINE
                elif title_regexp.match(line):
                    save_question()
                    create_question(line)
                    state = State.TITLE
                else:
                    question['text'] += '\n' + line  # multi-line question
                    state = State.QUESTION
            elif state == State.EMPTY_LINE:
                if len(line) == 0:
                    pass
                elif title_regexp.match(line):
                    create_question(line)
                    state = State.TITLE
                else:
                    save_group()
                    create_group(line)
                    state = State.GROUP_TITLE
            else:
                raise NotImplementedError

    if question['title']:
        save_question()

    if group['title']:
        save_group()

    return groups, group_types


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--questions_per_group', type=int,
                        default=1,
                        help='amount of questions to peek from each group, default = 1')
    parser.add_argument('--groups_count', type=int,
                        default=None,
                        help='amount of groups to peek from, default - all groups')
    parser.add_argument('--formal_questions_count', type=int,
                        default=None,
                        help='amount of items per ticket (one item can contain 1 ot more questions), '
                             'default = groups_count')
    parser.add_argument('--tickets_count', type=int,
                        default=30,
                        help='total amount of tickets, default = 30')
    parser.add_argument('--groups', type=str,
                        default=None,
                        help='groups to use')
    parser.add_argument('--input', type=str,
                        default='questions.txt',
                        help='input filename')
    parser.add_argument('--out', type=str,
                        default='tickets.docx',
                        help='output filename')
    parser.add_argument('--title', type=str,
                        default='Разработка интернет-приложений',
                        help='submission date (dd.MM.yyyy)')
    parser.add_argument('--date', type=str,
                        default='11.12.2016',
                        help='submission date (dd.MM.yyyy)')
    args = parser.parse_args()
    args.date = datetime.datetime.strptime(args.date, '%d.%m.%Y')

    if not os.path.exists('out'):
        os.mkdir('out')
    generate(args,
             os.path.join('data', args.input),
             'data/template.docx',
             os.path.join('out', args.out))


if __name__ == '__main__':
    main()

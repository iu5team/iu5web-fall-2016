import argparse
from enum import Enum

import numpy as np
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


def save_to_docx(tickets, template_file, output_file):
    doc = DocxTemplate(template_file)
    context = {
        'tickets': tickets
    }
    doc.render(context)
    doc.save(output_file)


def generate(args, questions_file, template_file, output_file):
    groups = parse_questions(questions_file)

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
    save_to_docx(tickets, template_file, output_file)


def parse_questions(questions_file):
    class State(Enum):
        BEGIN = 0
        GROUP_TITLE = 1
        TITLE = 2
        QUESTION = 3
        EMPTY_LINE = 4

    state = State.BEGIN

    groups = []

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
        group = {}

    def create_group(title):
        group['title'] = title
        group['questions'] = []

    with open(questions_file, encoding='utf-8') as f:
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

    return groups


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
    args = parser.parse_args()

    generate(args, 'data/questions.txt', 'data/template.docx', 'data/tickets.docx')


if __name__ == '__main__':
    main()

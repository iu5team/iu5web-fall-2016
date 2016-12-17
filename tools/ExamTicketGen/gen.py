import xml.etree.ElementTree as ET
import numpy as np
from docxtpl import DocxTemplate


def array_split(arr, chunks):
    result = []
    chunk_len = np.math.ceil(len(arr) / chunks)

    for i in range(chunks):
        result.append(arr[i * chunk_len:i * chunk_len + chunk_len])

    return result


def print_to_stdout(formal_questions):
    for i, fq in enumerate(formal_questions):
        print(i + 1)
        for q in fq:
            print('{}: {} {}'.format(q['group'], q['title'], q['text']))
        print('-----')


def save_to_docx(tickets, template_file, output_file):
    doc = DocxTemplate(template_file)
    context = {
        'tickets': tickets
    }
    doc.render(context)
    doc.save(output_file)


def generate(xml_file, template_file, output_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    groups = root.find('groups')
    meta = root.find('meta')

    questions_per_group = int(meta.attrib.get('questions_per_group', 1))
    groups_count = int(meta.attrib.get('groups_count', len(groups)))
    formal_questions_count = int(meta.attrib.get('formal_questions_count', groups_count))
    tickets_count = int(meta.attrib.get('tickets_count', 30))

    tickets = []
    for i in range(tickets_count):
        selected_groups = []
        ids = np.random.choice(len(groups), groups_count, False)
        ids.sort()
        for _id in ids:
            selected_groups.append(groups[_id])

        # collect all questions to one list
        questions = []
        for group in selected_groups:
            group_title = group.attrib['title']
            questions_in_group = len(group)
            group_questions = group.findall('question')
            ids = np.random.choice(len(group_questions), min(questions_in_group, questions_per_group), False)
            for _id in ids:
                title = group_questions[_id].attrib['title']
                text = group_questions[_id].text
                questions.append({
                    'title': title,
                    'text': text.strip(),
                    'group': group_title
                })

        formal_questions = array_split(questions, formal_questions_count)
        tickets.append({
            'formal_questions': formal_questions
        })

    # print_to_stdout(formal_questions)
    save_to_docx(tickets, template_file, output_file)


def main():
    generate(open('data/pool.xml', encoding='utf8'), 'data/template.docx', 'data/tickets.docx')


if __name__ == '__main__':
    main()

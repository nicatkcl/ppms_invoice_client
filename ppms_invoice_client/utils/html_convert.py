# -*- coding: utf-8 -*-

import os
from jinja2 import Environment, FileSystemLoader


TEMPLATE_PATH = os.path.abspath(
    os.path.join(os.path.dirname( __file__ ), '..', 'templates')
)
TEMPLATE_ENVIRONMENT = Environment(
    autoescape=False,
    loader=FileSystemLoader(TEMPLATE_PATH),
    trim_blocks=False)


def render_template(template_filename, context):
    return TEMPLATE_ENVIRONMENT.get_template(template_filename).render(context)


# input here should be a dictionary
def create_html(invoice_data, save_invoice=False):
    context = {
        'invoice_ref': invoice_data['invoice_ref'],
        'invoice_date': invoice_data['invoice_date'],
        'invoice_path': invoice_data['invoice_path'],
        'group': invoice_data['group'],
        'autonomous_sessions': invoice_data['autonomous_sessions'],
        'assisted_sessions': invoice_data['assisted_sessions'],
        'training_sessions': invoice_data['training_sessions'],
        'autonomous_charge': invoice_data['autonomous_charge'],
        'assisted_charge': invoice_data['assisted_charge'],
        'training_charge': invoice_data['training_charge'],
        'total': invoice_data['final_charge'],
        'fee_flag': invoice_data['fee_flag'],
        'subsidy_flag': invoice_data['subsidy_flag'],
        'message': invoice_data['message'],
        'columns': invoice_data['columns']
    }

    invoice_dir = os.path.dirname(invoice_data['invoice_path'])
    if not os.path.exists(invoice_dir):
        os.makedirs(invoice_dir)

    html = render_template('invoice_template.html', context)
    if save_invoice:
        with open(invoice_data['invoice_path'], 'w') as f:        
            f.write(html)

    return html


def main():
    create_html()


if __name__ == "__main__":
    main()

import os
import sys

html_files = ['index.html', 'anti_ia_detector_web.html', 'factcheck_web.html', 'success.html']
for f in html_files:
    if not os.path.exists(f):
        print('ERROR: {} not found'.format(f))
        sys.exit(1)
    with open(f, 'r', encoding='utf-8') as fp:
        content = fp.read()
        if '<html' not in content.lower():
            print('ERROR: {} does not appear to be valid HTML'.format(f))
            sys.exit(1)
    print('OK: {}'.format(f))
print('All HTML files validated')
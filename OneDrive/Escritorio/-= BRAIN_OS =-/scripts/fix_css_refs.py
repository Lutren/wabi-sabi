import os
import re

files = ['index.html', 'anti_ia_detector_web.html', 'factcheck_web.html', 'success.html']
base = r'C:\Users\L-Tyr\OneDrive\Escritorio\-= BRAIN_OS =-\apps\medioevo-tools'

for f in files:
    path = os.path.join(base, f)
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as fp:
            content = fp.read()
        if '../_shared/brainos-ui.css' in content:
            content = content.replace('../_shared/brainos-ui.css', '_shared/brainos-ui.css')
            with open(path, 'w', encoding='utf-8') as fp:
                fp.write(content)
            print('Fixed: {}'.format(f))
        else:
            print('No change needed: {}'.format(f))
    else:
        print('FILE NOT FOUND: {}'.format(f))
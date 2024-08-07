# Generates the Tracerecord playlist README.md file based on the seed JSON file.
# Created 2024-08-07

from num2alpha import Num2Alpha
import json

template_header = '''
# tr
All the personal musical taste and playlists known as "Tracerecord" combined into one single repository for accessibility
'''.strip()

template_yt_link = '''
<blockquote> <a href="%%%URL%%%"><svg xmlns="http://www.w3.org/2000/svg" width="1.43em" height="1em" viewBox="0 0 256 180"><path fill="#e01b24" d="M250.346 28.075A32.18 32.18 0 0 0 227.69 5.418C207.824 0 127.87 0 127.87 0S47.912.164 28.046 5.582A32.18 32.18 0 0 0 5.39 28.24c-6.009 35.298-8.34 89.084.165 122.97a32.18 32.18 0 0 0 22.656 22.657c19.866 5.418 99.822 5.418 99.822 5.418s79.955 0 99.82-5.418a32.18 32.18 0 0 0 22.657-22.657c6.338-35.348 8.291-89.1-.164-123.134" /><path fill="white" d="m102.421 128.06l66.328-38.418l-66.328-38.418z" /></svg></a> &nbsp;&nbsp; Established %%%DATE%%% </blockquote>
'''.strip()

content = ''

seed_json = '/ssynthesia/ghostcity/git-pub/tr/generator/seed.json'
with open(seed_json, 'r') as fi:
    j = json.load(fi)

# Convert month string in integer to month locale.
month_locale = {
    '01': 'January',
    '02': 'February',
    '03': 'March',
    '04': 'April',
    '05': 'May',
    '06': 'June',
    '07': 'July',
    '08': 'August',
    '09': 'September',
    '10': 'October',
    '11': 'November',
    '12': 'December'
}

for a in j['tr-data']:
    a_pos = j['tr-data'].index(a)
    
    # The "ABC" ordered list index.
    abc_index = Num2Alpha(echo=False).convert(a_pos + 1).upper()
    
    content += f"# {abc_index}. {a['title']}\n"
    content += f"_{a['desc']}_\n"
    content += '\n'
    
    i = 0
    for b in a['content']:
        # Convert the date string into date locale.
        date = b['date-est'].split('.')
        Y = date[0]
        M = date[1]
        D = date[2]
        
        date_out = ''
        
        # No "else" expression is required. The data is ensured to be valid and consistent.
        if M != 'nn' and D != 'nn':
            date_out += month_locale[M] + ' ' + str(int(D)) + ', ' + Y
        elif M != 'nn' and D == 'nn':
            date_out += month_locale[M] + ' ' + Y
        elif M == 'nn' and D == 'nn':
            date_out += Y
        
        content += f"### {i+1}. **{b['title']}**\n"
        content += '\n' + template_yt_link.replace('%%%URL%%%', b['url']).replace('%%%DATE%%%', date_out) + '\n'
        content += '\n'
        
        # Append the name of songs in this playlist.
        for c in b['songs']:
            content += f'- **{c[0]}** — {c[1]}\n'
        content += '\n'
        
        # Append the playlist's personal story.
        content += f"_{b['stories']}_"
        content += '\n\n'
        
        # Next iteration.
        i += 1

# Write the compiled markdown file into an external file.
output_file = '/ssynthesia/ghostcity/git-pub/tr/README.md'
with open(output_file, 'w') as fo:
    fo.write(template_header + '\n')
    fo.write('\n')
    fo.write(content)

# Done.

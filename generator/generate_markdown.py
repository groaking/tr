# Generates the Tracerecord playlist README.md file based on the seed JSON file.
# Created 2024-08-07

from num2alpha import Num2Alpha
import json

template_header = '''
# tr
All the personal musical taste and playlists known as "Tracerecord" combined into one single repository for accessibility
'''.strip()

template_yt_link = '> [![YT](https://raw.githubusercontent.com/groaking/tr/main/youtube_icon.svg)](%%%URL%%%) &nbsp;&nbsp; Established %%%DATE%%%'

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

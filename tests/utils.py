def generate_fixture_from_tag_file(tag_file):
  # generate a dummy tags file to feed to database
  with open(tag_file, 'r') as f:
    generate_fixture_from_tag_string(f.read())

def generate_fixture_from_tag_string(tag_string):
  # generate a dummy tags file to feed to database

  def parse_tags(lines):
    return [
      tuple(map(lambda x: x.strip(), line.split('\t')))
      for line in lines.split('\n')
      if line.strip() and '\t' in line
    ]

  data = parse_tags(tag_string)
  for ddt in data:
    with open(ddt[0], 'w') as f:
      f.write(ddt[1])

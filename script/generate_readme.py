from pathlib import Path
import re

README_FILE = 'README.md'
TITLE_CATALOGUE = '## Catalogue'
SPLIT_TITLE = '<!--title-->'
SPLIT_TILE = '<!--tile-->'
EXCLUDE_DIR = ['script', 'vr/openxr/monado/performance/project/OpenXR-SDK-Source', 'language/c++/c++primer']
RE_TITLE_FORMAT = re.compile('<center>\s*<h1>(.*)</h1>.*', re.DOTALL)
RE_SECOND_TITLE_FORMAT = '## '
RE_THIRD_TITLE_FORMAT = '### '
TITLE_FORMAT = '{} {}\n\n'
CONTETN_FORMAT = '* {}\n\n'
SECOND_CONTETN_FORMAT = '  * {}\n\n'

CATALOGUE_FORMAT = '{}\n<ul style="margin-top:0px;">{}</ul>\n'
DETAILS_SUMMARY = '<details><summary><a href="{}">{}</a></summary><ul style="margin-top:0px;">{}</ul></details>\n\n'
HTML_CONTENT_FORMART = '<li><a href="{}">{}</a></li>\n'
HTML_SECOND_CONTENT_FORMART = '<ul style="margin-top:0px;">{}</ul>\n'
URL_FORMAT = '{}#{}'

CONFIG_CATALOGUE_DEPTH = 4
class ReadmeInfo:
    def __init__(self, root_path:Path, file_path:Path) -> None:
        self.name = file_path.parent.name
        self.root_path = root_path
        self.file_path = file_path
        self.catalogue = self.generate_catalogue()
        self.parent_list = self.generate_parent_list()

    def generate_catalogue(self):
        catalogue_list = [] 
        with open(self.file_path, 'r+', encoding='utf-8') as f:
            content = f.read()
        rst = RE_TITLE_FORMAT.match(content)
        if rst:
            self.name = rst.group(1).strip()
        cur_second_title = None
        cur_third_titles = []
        for line in content.split('\n'):
            if line.startswith(RE_SECOND_TITLE_FORMAT):
                if cur_second_title:
                    catalogue_list.append((cur_second_title, cur_third_titles))
                cur_second_title = line.replace(RE_SECOND_TITLE_FORMAT, '').strip()
                cur_third_titles = []
            elif line.startswith(RE_THIRD_TITLE_FORMAT):
                cur_third_titles.append(line.replace(RE_THIRD_TITLE_FORMAT, '').strip())
        if cur_second_title:
            catalogue_list.append((cur_second_title, cur_third_titles))
        return catalogue_list

    # Generate parent list as ['vr', 'openxr']
    def generate_parent_list(self):
        relative_path = self.file_path.relative_to(self.root_path)
        parent_list = [i.name for i in relative_path.parents[::-1]][1:]
        return parent_list

    def __str__(self) -> str:
        return str(self.file_path.relative_to(self.root_path))

        
    def __len__(self):
        return 0 
    
    def to_catalogue(self, title=None, url_pre=True):
        content = ''
        for item in self.catalogue[1:] if title else self.catalogue:
            content += HTML_CONTENT_FORMART.format(URL_FORMAT.format(str(self) if url_pre else '', item[0]), item[0])
            if len(item[1]) > 0:
                second_content = ''
                for cata in item[1]:
                    second_content += HTML_CONTENT_FORMART.format(URL_FORMAT.format(str(self) if url_pre else '', cata), cata)
                content += HTML_SECOND_CONTENT_FORMART.format(second_content)
        if title:
            return CATALOGUE_FORMAT.format(title, content)
        return DETAILS_SUMMARY.format(str(self), title if title else self.name, content) 

def get_title_and_tile(content):
    title = content.split(SPLIT_TITLE)[0].strip()
    tile = content.split(SPLIT_TILE)[-1].strip()
    return title, tile

def generate_catalogue(root_path:Path):
    catalogue_tree = {}
    for readme in root_path.rglob(README_FILE):
        # Skip generated README in root dir.
        if str(readme.parent.absolute) == str(root_path.absolute):
            continue
        # Skip README in EXCLUDE_DIR
        exclude = False 
        for exclude_dir in EXCLUDE_DIR:
            exclude_path = root_path.joinpath(exclude_dir) 
            try:
                readme.relative_to(exclude_path)
                exclude = True 
                break
            except:
                print(readme, "is not in", exclude_path)  
        if exclude:
            print("Skip", readme)
            continue

        readme_info = ReadmeInfo(root_path, readme)
        # Put ReadmeInfo in tree
        node = None
        parent_node = None
        for parent in readme_info.parent_list:
            if parent_node == None:
                parent_node = catalogue_tree
            node = parent_node.get(parent)
            if node is None:
                parent_node[parent] = {}
            parent_node = parent_node.get(parent)
        if parent_node is None:
            parent_node = {}
        parent_node[README_FILE] = readme_info
    return catalogue_tree

def print_tree(catalogue_tree, index=0):
    for key, value in catalogue_tree.items():
        print("    " * index, key)
        if isinstance(value, dict):
            print_tree(value, index + 1)    
        else:
            print("    " * index, value)

def generate_catalogue_content(catalogue, pre_key='', index=3):
    file_content = ''
    # TODO use class to sort
    for key, value in sorted(catalogue.items(), key=lambda x: len(x[1])):
        # title = pre_key + '/' + key if pre_key else key
        title = key
        if isinstance(value, ReadmeInfo):
            if (len(value.catalogue) > 0):
                file_content += value.to_catalogue()
        # elif len(value) > 1:
        #     # If we have more children, just print the title.
        #     if index <= CONFIG_CATALOGUE_DEPTH:
        #         file_content += TITLE_FORMAT.format('#' * index, title)
        #     file_content += generate_catalogue_content(value, index=(index + 1))
        else:
            if index <= CONFIG_CATALOGUE_DEPTH:
                file_content += TITLE_FORMAT.format('#' * index, title)
            file_content += generate_catalogue_content(value, pre_key=title, index=(index + 1))
    return file_content

            
def generate_readme(root_path, readme_path, title, catalogue, tile):
    catalogue_content = generate_catalogue_content(catalogue)
    main_readme_info = ReadmeInfo(root_path, readme_path) 
    with open(readme_path, 'w+', encoding='utf-8') as f:
        f.write(title + '\n')
        f.write(SPLIT_TITLE + "\n")
        f.write(main_readme_info.to_catalogue(TITLE_CATALOGUE, False) + '\n')
        f.write('## Content\n')
        f.write(catalogue_content)
        f.write(SPLIT_TILE + "\n")
        f.write(tile)

if __name__ == '__main__':
    root_path = Path(__file__).parent.parent
    readme_path = root_path.joinpath(README_FILE)
    assert readme_path.exists(), "Can not find README.md"
    with open(readme_path, "r+", encoding='utf-8') as f:
        content = f.read()
    title, tile = get_title_and_tile(content)
    catalogue = generate_catalogue(root_path)
    generate_readme(root_path, readme_path ,title, catalogue, tile)
    # TODO recall for update catalogue
    generate_readme(root_path, readme_path ,title, catalogue, tile)
    print("Success to generate RAEDME.md")

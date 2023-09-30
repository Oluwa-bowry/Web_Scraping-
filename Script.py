#! python3

# import libraries
import webbrowser
import requests
from bs4 import BeautifulSoup
from jinja2 import Template
import time


def main():
    startTime = time.time()
    
    # Step 1: Get URL from input area
    url = input("Enter URL: ")
    
    print('Googling...') # display text while downloading the Google page
    
    # Step 2: Navigate to the URL
    webbrowser.open(url)
    
    # Step 3: Find elements with bolded text
    response = requests.get(url)
    try:
        response.raise_for_status()
        print('Http response code: %s' % str(response.status_code))

        soup = BeautifulSoup(response.content, 'html.parser')
        bold_elements = soup.find_all('h3')
        
        if len(bold_elements) > 0:
            print('Bold elements located')

            content = ""
            for element in bold_elements:
                # Extract content of the parent div container
                parent_div_content = element.find_parent('div').get_text()
                content += parent_div_content + "\n\n"

            print('Total length of the container div: %s' % len(content))
            
            # Step 4: Sending content to another page using Jinja2 template
            template_str = '''
            <h2>Extracted Content:</h2>
            <pre>{{ content }}</pre>
            '''
            template = Template(template_str)
            rendered_template = template.render(content=content)
            
            with open('output.html', 'w', encoding='utf-8') as f:
                f.write(rendered_template)
            
            # Open the generated HTML file in the default web browser
            webbrowser.open('output.html')
        else:
            print('Webpage does not have bold elements')
        
        
    except Exception as exc:
        print('There was a problem: %s' % (exc))

    endTime = time.time()
    
    print('Took %s seconds to calculate.' % (endTime - startTime))
    

if __name__ == "__main__":
    main()

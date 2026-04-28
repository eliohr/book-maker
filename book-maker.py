from pypdf import PdfReader, PdfWriter, PageObject
import math

import logging
# I was getting clutter in the output from pypdf having its own issues with pdf data
logging.disable(logging.WARNING)

name = input("\nmove this file and the pdf you'd like to convert into the same folder and then navigate to that directory and then run this file and then enter the name of the pdf you'd like to convert (without file extension): ")
    
pdf_name = name + ".pdf"

def four_pager(input_pdf, output_pdf):
    
    reader = PdfReader(input_pdf)
    writer = PdfWriter()
    
    # i would like to add support for 2x2 and 8x8 printing as well. i feel pretty awesome about myself cause gemini couldn't figure out the page logic. but i guess probably claude could have. whatever...

    # the number of pages in the in the input pdf
    input_pages = reader.get_num_pages()
    
    # the number of single sheet sides (pages) in the output pdf
    sheet_sides = math.ceil((input_pages / 4))
    
    # the number of total sheets in the final booklet
    sheets = math.ceil(sheet_sides / 2)
    
    # the number of total pages (including blank ones at the end) in the final booklet
    rounded_pages = sheets * 8
    
    first_page = reader.pages[0]
    w = float(first_page.mediabox.width)
    h = float(first_page.mediabox.height)
    
    blank = PageObject.create_blank_page(width=w, height=h)

    #   i still need to create and scale the blank and instructions pages
    
    '''
    blank_reader = PdfReader("blank.pdf")
    blank_page = blank_reader.pages[0]
    blank.merge_page(blank_page)
        
    instructions_reader = PdfReader("instructions.pdf")
    instructions_page = instructions_reader.pages[0]
    writer.add_page(instructions_page)
    '''
    
    # for each page (for each single sheet side)
    for i in range(sheets):
        
        front = PageObject.create_blank_page(width=w*2, height=h*2)
        
        # for sheet i
        f_indices = [
            int((rounded_pages/4)-1 - (2*i)),   # top left
            int((rounded_pages/4)*3 + (2*i)),  # top right
            int((rounded_pages/2)-1 - (2*i)),  # bottom left
            int((rounded_pages/2) + (2*i))     # bottom right
        ]
        
        '''
        print("\nfront of sheet " + str(i) + " ")
        print(f_indices)
        '''
        
        try: front.merge_translated_page(reader.pages[f_indices[0]], 0, h, False)
        except IndexError: front.merge_translated_page(blank, 0, h, False)
        try: front.merge_translated_page(reader.pages[f_indices[1]], w, h, False)
        except IndexError: front.merge_translated_page(blank, 0, h, False)
        try: front.merge_translated_page(reader.pages[f_indices[2]], 0, 0, False)
        except IndexError: front.merge_translated_page(blank, 0, h, False)
        try: front.merge_translated_page(reader.pages[f_indices[3]], w, 0, False)
        except IndexError: front.merge_translated_page(blank, 0, h, False)
        
        back = PageObject.create_blank_page(width=w*2, height=h*2)
        
        # for sheet i
        b_indices = [
            int((rounded_pages/4)*3+1 + (2*i)),    # top left
            int((rounded_pages/4)-2 - (2*i)),      # top right
            int((rounded_pages/2)+1 + (2*i)),      # bottom left
            int((rounded_pages/2)-2 - (2*i))       # bottom right
        ]
        
        '''
        print("\nback of sheet " + str(i) + " ")
        print(b_indices)
        '''
        
        try: back.merge_translated_page(reader.pages[b_indices[0]], 0, h, False)
        except IndexError: back.merge_translated_page(blank, 0, h, False)
        try: back.merge_translated_page(reader.pages[b_indices[1]], w, h, False)
        except IndexError: back.merge_translated_page(blank, 0, h, False)
        try: back.merge_translated_page(reader.pages[b_indices[2]], 0, 0, False)
        except IndexError: back.merge_translated_page(blank, 0, h, False)
        try: back.merge_translated_page(reader.pages[b_indices[3]], w, 0, False)
        except IndexError: back.merge_translated_page(blank, 0, h, False)
        
        writer.add_page(front)
        writer.add_page(back)

    with open(output_pdf, "wb") as wb:
        writer.write(wb)
        
    return 0

four_pager(pdf_name, f"{name}-4x4_booklet.pdf")

print(f"\n{name}-4x4_booklet.pdf is your new document. to bind, cut it hamburger style, put the bottom half on top of the top half, staple along the middle, and fold. if the document is too long, \n")

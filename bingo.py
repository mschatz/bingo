#!/usr/bin/env python

import random
import argparse
from fpdf import FPDF
from PIL import Image
import os

def read_strings(file_path):
    """Read strings from a text file and return a list."""
    with open(file_path, 'r') as file:
        strings = [line.strip() for line in file if line.strip()]
    return strings

def generate_bingo_card(strings):
    """Generate a random 5x5 Bingo card from a list of strings."""
    if len(strings) < 24:
        raise ValueError("Not enough strings to generate a Bingo card (at least 24 required excluding the free square).")
    selected_strings = random.sample(strings, 24)
    bingo_card = [selected_strings[i:i + 5] for i in range(0, 20, 5)]
    middle_row = selected_strings[20:24]
    middle_row.insert(2, "FREE")  # Add the free square in the center
    bingo_card.insert(2, middle_row[:5])
    return bingo_card

def generate_multiple_bingo_cards(strings, num_boards):
    """Generate multiple random Bingo cards."""
    return [generate_bingo_card(strings) for _ in range(num_boards)]

def print_bingo_card(card):
    """Print the Bingo card to the console."""
    print("\nCosmic Cowpoke:")
    for row in card:
        print(" | ".join(f"{cell:15}" for cell in row))

def save_bingo_cards_as_pdf(cards, output_file, png_file):
    """Save multiple Bingo cards as a PDF."""
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    for card in cards:
        pdf.add_page()
        pdf.set_font("Arial", size=50)
        pdf.set_text_color(24, 43, 89)  # Dark blue (#182B59) for title
        pdf.cell(0, 20, "Cosmic Cowpoke", ln=True, align='C')
        pdf.set_text_color(0, 0, 0)  # Reset to black for the rest of the text
        pdf.set_font("Arial", size=10)
        pdf.ln(10)

        cell_width = 35
        cell_height = 35

        for row_index, row in enumerate(card):
            y_position = pdf.get_y()
            for col_index, cell in enumerate(row):
                x_position = 10 + col_index * cell_width
                pdf.set_xy(x_position, y_position)
                if cell == 'FREE':
                    pdf.set_fill_color(173, 216, 230)  # Light blue for FREE square
                    pdf.set_draw_color(0, 0, 139)  # Dark blue border
                    pdf.set_font("Arial", style="B", size=10)
                    pdf.multi_cell(cell_width, cell_height, cell, border=1, align='C', fill=True)
                    pdf.set_font("Arial", size=10)
                else:
                    pdf.set_fill_color(255, 255, 255)  # White fill for other cells
                    pdf.set_draw_color(0, 0, 139)  # Dark blue border
                    if len(cell) > 15:
                        words = cell.split()
                        wrapped_text = ''
                        line = ''
                        for word in words:
                            if len(line) + len(word) + 1 <= 15:
                                line += (word + ' ')
                            else:
                                wrapped_text += (line.strip() + '\n')
                                line = word + ' '
                        wrapped_text += line.strip()
                        lines = wrapped_text.count('\n') + 1
                        if (lines == 2):
                            wrapped_text = '\n' + wrapped_text + '\n' + '\n'
                            lines = 4
                        elif (lines == 3):
                            wrapped_text = '\n' + wrapped_text + '\n' + '\n'
                            lines = 5
                        pdf.multi_cell(cell_width, cell_height / lines, wrapped_text, border=1, align='C', fill=True)
                    else:
                        pdf.multi_cell(cell_width, cell_height, cell, border=1, align='C', fill=True,)
            pdf.set_y(y_position + cell_height)

        if png_file and os.path.exists(png_file):
            pdf.image(png_file, x=10, y=pdf.get_y() + 10, w=190)

    pdf.output(output_file)

def main():
    parser = argparse.ArgumentParser(description="Generate Bingo cards.")
    parser.add_argument("file", help="Path to the text file containing strings.")
    parser.add_argument("--num_boards", type=int, default=1, help="Number of Bingo boards to generate (default: 1).")
    parser.add_argument("--output", choices=["console", "pdf"], default="console",
                        help="Output format: console or pdf (default: console).")
    parser.add_argument("--pdf_file", default="bingo_card.pdf",
                        help="Output PDF file name (default: bingo_card.pdf).")
    parser.add_argument("--png_file", default=None, help="Path to a PNG file to include at the bottom of each page.")
    args = parser.parse_args()

    try:
        strings = read_strings(args.file)
        bingo_cards = generate_multiple_bingo_cards(strings, args.num_boards)

        if args.output == "console":
            for i, card in enumerate(bingo_cards, start=1):
                print(f"\nBingo Card {i}:")
                print_bingo_card(card)
        elif args.output == "pdf":
            save_bingo_cards_as_pdf(bingo_cards, args.pdf_file, args.png_file)
            print(f"Bingo cards saved to {args.pdf_file}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()

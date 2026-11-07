import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image as RLImage, Table, TableStyle, PageBreak
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

pdf_path = os.path.join(os.path.dirname(__file__), 'PES2UG24CS062_ANGELO_ARAKAL_LAB7.pdf')
doc = SimpleDocTemplate(
    pdf_path,
    pagesize=letter,
    leftMargin=36,
    rightMargin=36,
    topMargin=36,
    bottomMargin=36
)

styles = getSampleStyleSheet()

title_style = ParagraphStyle(
    'DocTitle',
    parent=styles['Normal'],
    fontName='Helvetica-Bold',
    fontSize=18,
    leading=22,
    textColor=colors.HexColor('#1E293B'),
    spaceAfter=4
)

subtitle_style = ParagraphStyle(
    'DocSubTitle',
    parent=styles['Normal'],
    fontName='Helvetica-Bold',
    fontSize=12,
    leading=15,
    textColor=colors.HexColor('#2563EB'),
    spaceAfter=10
)

meta_style = ParagraphStyle(
    'MetaText',
    parent=styles['Normal'],
    fontName='Helvetica',
    fontSize=9,
    leading=13,
    textColor=colors.HexColor('#334155')
)

h1_style = ParagraphStyle(
    'H1',
    parent=styles['Normal'],
    fontName='Helvetica-Bold',
    fontSize=13,
    leading=17,
    textColor=colors.HexColor('#1E293B'),
    spaceBefore=12,
    spaceAfter=6,
    keepWithNext=True
)

h2_style = ParagraphStyle(
    'H2',
    parent=styles['Normal'],
    fontName='Helvetica-Bold',
    fontSize=10.5,
    leading=14,
    textColor=colors.HexColor('#0F766E'),
    spaceBefore=8,
    spaceAfter=4,
    keepWithNext=True
)

body_style = ParagraphStyle(
    'Body',
    parent=styles['Normal'],
    fontName='Helvetica',
    fontSize=9,
    leading=13,
    textColor=colors.HexColor('#1F2937'),
    spaceAfter=5
)

bullet_style = ParagraphStyle(
    'Bullet',
    parent=body_style,
    leftIndent=14,
    firstLineIndent=-10,
    spaceAfter=4
)

story = []

# Title & Metadata
story.append(Paragraph('LAB 7: Fuzzing for Input Validation Bugs', title_style))
story.append(Paragraph('Software Engineering Lab Report & Verification Deliverables', subtitle_style))

meta_data = [
    [Paragraph('<b>Student Name:</b> Angelo Arakal', meta_style), Paragraph('<b>SRN:</b> PES2UG24CS062', meta_style)],
    [Paragraph('<b>Assigned Repository:</b> L6_L7_58_restaurant_bill', meta_style), Paragraph('<b>Module Under Test:</b> restaurant_bill_parser.py', meta_style)],
    [Paragraph('<b>Testing Tool:</b> Hypothesis Fuzzing Framework', meta_style), Paragraph('<b>Date:</b> November 7, 2026', meta_style)]
]
t = Table(meta_data, colWidths=[270, 270])
t.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F8FAFC')),
    ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#CBD5E1')),
    ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
    ('TOPPADDING', (0,0), (-1,-1), 5),
    ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ('LEFTPADDING', (0,0), (-1,-1), 8),
    ('RIGHTPADDING', (0,0), (-1,-1), 8),
]))
story.append(t)
story.append(Spacer(1, 8))

# Overview
story.append(Paragraph('1. Overview & Objectives', h1_style))
story.append(Paragraph(
    'The goal of this laboratory exercise is to explore <b>property-based fuzz testing</b> using Python\'s '
    '<b>Hypothesis</b> library. Traditional unit testing often focuses on anticipated happy paths or obvious corner cases, '
    'leaving latent input validation vulnerabilities unnoticed. Fuzzing generates hundreds to thousands of semi-random, '
    'unexpected, and malformed inputs to rigorously evaluate application robustness, crash resilience, and defensive input handling.',
    body_style
))

# Section 2: Screenshots
story.append(Paragraph('2. Verification Screenshots (SS1 to SS4)', h1_style))
story.append(Paragraph(
    'The following screenshots document the step-by-step fuzzing lifecycle: running the initial buggy module, '
    'discovering failure modes with Hypothesis, hardening the codebase against unexpected inputs, and verifying that '
    'all property tests pass successfully.',
    body_style
))

img_w = 540
script_dir = os.path.dirname(__file__)
ss1_img = os.path.join(script_dir, 'screenshots', 'SS1_buggy_module_run.png')
ss2_img = os.path.join(script_dir, 'screenshots', 'SS2_fuzz_tests_failing.png')
ss3_img = os.path.join(script_dir, 'screenshots', 'SS3_fixed_module_run.png')
ss4_img = os.path.join(script_dir, 'screenshots', 'SS4_fuzz_tests_passing.png')

# SS1
story.append(Paragraph('<b>SS1: Running the Buggy Module (python restaurant_bill_parser.py)</b>', h2_style))
story.append(Paragraph('Demonstrates normal execution with expected well-formed inputs (*paneer tikka*, 250,180,320, 1200/4).', body_style))
story.append(RLImage(ss1_img, width=img_w, height=img_w * (250/880)))
story.append(Spacer(1, 10))

# SS2
story.append(PageBreak())
story.append(Paragraph('<b>SS2: Hypothesis Fuzz Tests Failing on Buggy Module (pytest test_restaurant_bill_parser.py)</b>', h2_style))
story.append(Paragraph('Demonstrates Hypothesis generating edge-case inputs (None, empty strings, missing delimiters, zero division) that cause unhandled exceptions (AttributeError, ValueError, ZeroDivisionError).', body_style))
story.append(RLImage(ss2_img, width=img_w, height=img_w * (580/880)))
story.append(Spacer(1, 10))

# SS3
story.append(PageBreak())
story.append(Paragraph('<b>SS3: Running the Fixed Module (python restaurant_bill_parser.py)</b>', h2_style))
story.append(Paragraph('Demonstrates that the hardened implementation preserves correct functionality for legitimate inputs while safely processing malformed data.', body_style))
story.append(RLImage(ss3_img, width=img_w, height=img_w * (250/880)))
story.append(Spacer(1, 10))

# SS4
story.append(Paragraph('<b>SS4: Hypothesis Fuzz Tests Passing on Fixed Module (pytest test_restaurant_bill_parser.py)</b>', h2_style))
story.append(Paragraph('Confirms that all three functions successfully pass 100% of property-based fuzz tests across thousands of generated inputs without crashing.', body_style))
story.append(RLImage(ss4_img, width=img_w, height=img_w * (260/880)))
story.append(Spacer(1, 12))

# Section 3: Reflection Questions
story.append(PageBreak())
story.append(Paragraph('3. Reflection & Technical Analysis', h1_style))

# Question 1
story.append(Paragraph('Question 1: What bugs/exceptions were identified by Hypothesis in each of the three functions?', h2_style))
story.append(Paragraph(
    'Fuzzing with Hypothesis exposed several critical input validation failures and unhandled runtime exceptions in all three functions of the buggy module:',
    body_style
))
story.append(Paragraph(
    '&bull; <b>clean_dish_name(name):</b> Assumed <code>name</code> was always a valid string. When passed <code>None</code> or non-string objects, '
    'calling <code>name.strip()</code> immediately crashed with an <code>AttributeError: \'NoneType\' object has no attribute \'strip\'</code>.',
    bullet_style
))
story.append(Paragraph(
    '&bull; <b>parse_item_prices(text):</b> Assumed comma-separated values of valid integers. When passed <code>None</code>, <code>text.split(\',\')</code> raised '
    '<code>AttributeError</code>. When passed an empty string <code>""</code> or trailing/consecutive commas like <code>"1,,3"</code>, <code>int("")</code> '
    'raised <code>ValueError: invalid literal for int() with base 10: \'\'</code>. Non-numeric text (e.g. <code>"one,two"</code>) also caused <code>ValueError</code>.',
    bullet_style
))
story.append(Paragraph(
    '&bull; <b>split_amount(text):</b> Made multiple fragile assumptions regarding input format and numerical values. When passed <code>None</code>, '
    '<code>split(\'/\')</code> failed with <code>AttributeError</code>. When passed strings lacking a slash (e.g. <code>""</code> or <code>"100"</code>) '
    'or containing multiple slashes (e.g. <code>"1/2/3"</code>), tuple unpacking <code>total, people = text.split(\'/\')</code> raised <code>ValueError</code>. '
    'When non-integer strings were provided (e.g. <code>"/"</code> or <code>"abc/xyz"</code>), <code>int()</code> raised <code>ValueError</code>. '
    'Crucially, when <code>people = 0</code> (e.g. <code>"1200/0"</code>), integer division caused a fatal <code>ZeroDivisionError</code>.',
    bullet_style
))

story.append(Spacer(1, 6))

# Question 2
story.append(Paragraph('Question 2: What edge cases and minimal failing examples were discovered, and why did manual tests miss them?', h2_style))
story.append(Paragraph(
    'Hypothesis employs an automated test-case reduction algorithm called <b>shrinking</b>. When a failure is detected, Hypothesis simplifies '
    'the input to find the smallest, most concise counterexample that reproduces the defect:',
    body_style
))
story.append(Paragraph(
    '&bull; <b>Minimal Counterexamples Discovered:</b><br/>'
    '  - <code>clean_dish_name</code>: <code>s = None</code> (minimal null reference).<br/>'
    '  - <code>parse_item_prices</code>: <code>s = ""</code> and <code>s = None</code> (empty string and null inputs).<br/>'
    '  - <code>split_amount</code>: <code>s = ""</code> (missing delimiter), <code>s = "/"</code> (empty numerical tokens), and <code>s = None</code>.',
    bullet_style
))
story.append(Paragraph(
    '&bull; <b>Why Manual Tests Miss Them:</b> Developers write unit tests with cognitive bias, anticipating typical workflow inputs '
    '("happy paths") and standard edge cases (e.g. negative numbers or large values). Manual testing rarely tests non-standard Unicode, '
    'unintended delimiter counts, null pointers, or empty string splits across all parameters simultaneously. Fuzzing explores the complete input '
    'domain systematically, finding edge cases that humans rarely imagine.',
    bullet_style
))

story.append(Spacer(1, 6))

# Question 3
story.append(Paragraph('Question 3: How was defensive programming applied to harden the functions, and what are the benefits of fuzz testing?', h2_style))
story.append(Paragraph(
    'To harden the application against all invalid and malformed inputs, we refactored each function using defensive programming principles:',
    body_style
))
story.append(Paragraph(
    '&bull; <b>Type & Null Guards:</b> Checked <code>isinstance(input, str)</code> and <code>bool(input)</code> upfront, returning safe default '
    'values (<code>""</code> for strings, <code>[]</code> for lists, and <code>0</code> for numerical totals) instead of allowing unchecked execution.',
    bullet_style
))
story.append(Paragraph(
    '&bull; <b>Safe Token Parsing & Resilient Iteration:</b> In <code>parse_item_prices</code>, individual tokens are stripped and wrapped in '
    'a <code>try-except (ValueError, TypeError)</code> block, skipping malformed entries while retaining valid integers.',
    bullet_style
))
story.append(Paragraph(
    '&bull; <b>Delimiter Count & Arithmetic Safety:</b> In <code>split_amount</code>, verified <code>len(parts) == 2</code> before unpacking, '
    'and explicitly checked <code>if people == 0</code> alongside catching <code>ZeroDivisionError</code> and <code>ValueError</code>.',
    bullet_style
))
story.append(Paragraph(
    '&bull; <b>Benefits of Property-Based Fuzz Testing:</b> Fuzz testing ensures high reliability and security by discovering crash vulnerabilities, '
    'denial-of-service conditions, and injection surfaces before code is deployed. Combining Hypothesis property tests with defensive programming '
    'guarantees software resilience across the entire possible input space.',
    bullet_style
))

doc.build(story)
print('Generated PDF successfully at:', pdf_path)

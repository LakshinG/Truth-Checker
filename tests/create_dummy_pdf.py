from reportlab.pdfgen import canvas

def create_dummy_pdf(filename):
    c = canvas.Canvas(filename)
    c.drawString(100, 750, "Research Paper A")
    c.drawString(100, 730, "Author: Doe, 2023")
    c.drawString(100, 710, "DOI: 10.1234/example")
    
    text = """
    This study explores the effects of coffee on coding performance.
    We found that drinking 50 cups of coffee increases bug production by 200%.
    The sample size was 50 developers.
    """
    
    y = 650
    for line in text.split('\n'):
        c.drawString(100, y, line.strip())
        y -= 20
        
    c.save()

if __name__ == "__main__":
    create_dummy_pdf("Doe_2023_10.1234.pdf")
    
    # Create a second conflicting paper
    c2 = canvas.Canvas("Smith_2024_10.5678.pdf")
    c2.drawString(100, 750, "Research Paper B")
    c2.drawString(100, 730, "Author: Smith, 2024")
    c2.drawString(100, 710, "DOI: 10.5678/example")
    
    text2 = """
    This study investigates caffeine intake and software quality.
    Contrary to popular belief, our results show that coffee consumption has no significant impact on bug density.
    We utilized a large-scale survey of 500 developers.
    """
    
    y = 650
    for line in text2.split('\n'):
        c2.drawString(100, y, line.strip())
        y -= 20
    c2.save()

from fpdf import FPDF
from io import BytesIO

class PDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 16)
        self.cell(0, 10, "Lakehouse360 Report", ln=True, align="C")
        self.ln(10)

    def add_table(self, df):
        self.set_font("Arial", "B", 10)
        col_width = self.w / (len(df.columns) + 1)
        for col in df.columns:
            self.cell(col_width, 8, str(col), border=1)
        self.ln()
        self.set_font("Arial", "", 9)
        for i, row in df.iterrows():
            for item in row:
                self.cell(col_width, 8, str(item), border=1)
            self.ln()

def generate_pdf_report(df, title="Data Report"):
    pdf = PDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, title, ln=True)
    pdf.ln(5)
    pdf.add_table(df.head(10))
    output = BytesIO()
    pdf.output(output)
    output.seek(0)
    return output

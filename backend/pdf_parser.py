import pdfplumber
import re
import json
from pathlib import Path
from typing import List, Dict


def clean_text(text: str) -> str:
    """Cleans whitespace and formatting from text."""
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def extract_paragraph_chunks(pdf_path: str, chunk_size: int = 300) -> List[Dict]:
    """Extracts paragraph-level text chunks from PDF for embedding."""
    chunks = []
    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages, start=1):
            text = clean_text(page.extract_text() or "")
            paragraphs = [p for p in text.split('\n') if p.strip()]
            
            buffer = ""
            for para in paragraphs:
                buffer += " " + para
                if len(buffer.split()) > chunk_size:
                    chunks.append({
                        "text": buffer.strip(),
                        "page": page_num,
                        "source": Path(pdf_path).name
                    })
                    buffer = ""
            if buffer:
                chunks.append({
                    "text": buffer.strip(),
                    "page": page_num,
                    "source": Path(pdf_path).name
                })
    return chunks


def extract_structured_clauses(pdf_path: str) -> List[Dict]:
    """Extracts clauses based on numbered sections using regex."""
    clauses = []
    current_clause = None

    section_pattern = re.compile(r'(section\s+)?(\d+(\.\d+)*)(:|-)?\s+(.*)', re.IGNORECASE)

    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages, start=1):
            text = clean_text(page.extract_text() or "")
            lines = text.split('\n')

            for line in lines:
                match = section_pattern.match(line.strip())
                if match:
                    # Save previous clause
                    if current_clause:
                        clauses.append(current_clause)

                    # Start new clause
                    section = match.group(2)
                    title = match.group(5)
                    current_clause = {
                        "section": section,
                        "title": title,
                        "text": "",
                        "page": page_num,
                        "source": Path(pdf_path).name
                    }
                elif current_clause:
                    current_clause["text"] += " " + line.strip()

    # Final clause
    if current_clause:
        clauses.append(current_clause)

    return clauses


def save_jsonl(data: List[Dict], out_path: str):
    with open(out_path, 'w', encoding='utf-8') as f:
        for item in data:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")


def save_json(data: List[Dict], out_path: str):
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def process_pdf(pdf_path: str, out_dir: str):
    """Main function to extract and save both chunks and clauses."""
    Path(out_dir).mkdir(parents=True, exist_ok=True)

    chunks = extract_paragraph_chunks(pdf_path)
    clauses = extract_structured_clauses(pdf_path)

    save_jsonl(chunks, Path(out_dir) / "extracted_chunks.jsonl")
    save_json(clauses, Path(out_dir) / "extracted_clauses.json")

    print(f"[✓] Extracted {len(chunks)} chunks and {len(clauses)} clauses from {pdf_path}")


if __name__ == "__main__":
    # 🔧 Change these paths as needed
    pdf_file = "policy_pdf.pdf"
    output_dir = "data"

    process_pdf(pdf_file, output_dir)

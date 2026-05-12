from datetime import datetime
import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from PyPDF2 import PdfReader
from fpdf import FPDF

load_dotenv()

def extract_text_from_pdf(pdf_file): # pdf olvaso letrehozasa
    reader = PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def create_pdf_output(content): # pdf keszito letrehozasa
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12) 
    pdf.multi_cell(0, 10, content.encode('latin-1', 'replace').decode('latin-1'))
    return pdf.output(dest='S').encode('latin-1')

st.set_page_config(page_title="MI Tanulási Segéd", layout="wide")

if "result" not in st.session_state:
    st.session_state.result = "" #memoria inicializalas

if "history" not in st.session_state:
    st.session_state.history = []

st.title("📚 Intelligens Tanulási Segéd")

with st.sidebar: #oldalsav letrehozasa
    st.header("⚙️ Beállítások")
    model = st.selectbox("Modell", ["llama-3.3-70b-versatile", "llama-3.1-8b-instant"])
    temp = st.slider("Temperature", 0.0, 1.0, 0.3) 
    max_tokens = st.slider("Max Tokens", 500, 2000, 1000)

    st.markdown("---")
    if st.button("🗑️ Elemzés törlése", use_container_width=True): #eredmenytorlo gomb
        st.session_state.result = ""
        st.rerun() 

tab1, tab2 = st.tabs(["📝 Elemzés", "📜 Korábbi elemzések"]) # tab-ok letrehozasa

with tab1:
    uploaded_file = st.file_uploader("Töltsd fel a jegyzetet (PDF)", type="pdf") # fajl kezelese

    if st.button("Elemzés indítása", type="primary"):
        if uploaded_file is not None: # ha felvan toltve egy file
            with st.spinner("Az MI elemzi a dokumentumot..."): # "toltokepernyo"
                try:
                    # szoveg kinyerese a pdfbol
                    text_to_analyze = extract_text_from_pdf(uploaded_file)
                    
                    # hivas
                    llm = ChatGroq(model=model, temperature=temp, max_tokens=max_tokens)
                    
                    prompt = f"""
                    Te egy tapasztalt egyetemi professzor vagy. 
                    A feladatod az alábbi szöveg elemzése:
                    {text_to_analyze[:5000]}
                    Instrukciók:
                    1. Készíts egy pontos összefoglalót.
                    2. Gyűjtsd ki a legfontosabb fogalmakat.
                    3. Generálj 3 ellenőrző kérdést példa alapján:
                    Példa: "Mi a sejtmag feladata? a) energia b) irányítás c) raktározás"
                    
                    Lépésről lépésre elemezd a logikai összefüggéseket.
                    """
                    
                    response = llm.invoke(prompt) # uzenet elkuldese
                    st.session_state.result = response.content # eredmeny mentese a memoriaba

                    uj_bejegyzes = {
                        "idopont": datetime.now().strftime("%H:%M:%S"),
                        "fajlnev": uploaded_file.name,
                        "tartalom": response.content
                        }
                    st.session_state.history.append(uj_bejegyzes) #eredmeny mentese historyba
                
                except Exception as e:
                    st.error(f"Hiba történt: {str(e)}") # hibakezeles
        else: # ha feltoltes nelkul ranyomunk a gombra
            st.warning("Előbb töltsd fel a PDF fájlt, különben nincs mit elemeznem!")

    if st.session_state.result: # eredmeny megjelenitese es letoltesi lehetoseg
        st.markdown("### 📋 Elemzési eredmények")
        st.write(st.session_state.result)
        #letoltes gomb
        pdf_bytes = create_pdf_output(st.session_state.result) # a kapott uzenet adatta alakitasa
        st.download_button(
            label="📥 Eredmények letöltése PDF-ben",
            data=pdf_bytes,
            file_name="elemzes.pdf",
            mime="application/pdf"
        )

with tab2: # elemzeshistory
    st.subheader("📜 Korábbi elemzések")

    if not st.session_state.history: # ha meg nem volt elemzes
        st.info("Még nincs mentett elemzés.")
    else:
        # reversed a sorrendforditas miatt kell, hogy az uj elemzes legyen mindig legfelul az oldalon
        for i, elem in enumerate(reversed(st.session_state.history)):
            with st.expander(f"🕒 {elem['idopont']} - {elem['fajlnev']}"): # a lenyilo ful letrehozasa
                st.write(elem['tartalom']) # csak akkor irja ki a tartalmat ill. a letoltes lehetoseget, ha levan nyitva
                
                # letoltogomb mindegyik elemhez
                pdf_adat = create_pdf_output(elem['tartalom'])
                st.download_button(
                    label=f"📥 Letöltés ({elem['idopont']})",
                    data=pdf_adat,
                    file_name=f"elemzes_{elem['idopont']}.pdf",
                    mime="application/pdf",
                    key=f"download_{i}" #egyedi kulcs minden gombnak, kulonben nem fut le
                )
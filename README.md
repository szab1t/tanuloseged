# 📚 Intelligens Tanulósegéd 
## Projektleírás
PDF fájlok elemzésére és összefoglalására szolgáló alkalmazás mesterséges intelligencia támogatással. Segít a tananyag gyors feldolgozásában és gyakorló kvízek generálásában.

## Funkciók
* **PDF feldolgozás:** Szöveg kinyerése feltöltött dokumentumokból.

* **Összefoglalás:** A mesterséges intelligencia rövid, lényegre törő összefoglalót készít.

* **Kvíz generálás:** Automatikus kérdések a tananyag alapján.

* **History:** Korábbi elemzések mentése és visszakeresése.

* **Letöltés:** Az eredmények elmenthetők PDF formátumban.

## Alkalmazott technológiák
* **Python:** Alapprogramozási nyelv.

* **Streamlit:** Webes felhasználói felület.

* **Groq Cloud:** Llama 3 nyelvi modell az elemzéshez.

* **LangChain:** Szövegfeldolgozó keretrendszer.

## Használat
1. Klónozd a tárolót
```
git clone https://github.com/szab1t/tanuloseged.git
```
2. Telepítsd a szükséges könyvtárakat
```
pip install -r requirements.txt
```
3. Hozz létre egy .env filet a gyökérmappádban, és add meg az API kulcsodat
4. Indítsd el az alkalmazást
```
streamlit run app.py
```

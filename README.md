# TagIT – Accessible AI-Tagged Markdown Search

TagIT je orodje, namenjeno **dostopnemu iskanju po vsebini** za slepe in slabovidne.**AI-tagging** vsebine omogoča hitro navigacijo po datotekah in odstavkih na osnovi ključnih pojmov, npr. #kvadratne_funkcije in #enačbe, ter dostop do specifičnih vsebinskih sklopov znotraj dokumenta.
---

## 🎯 Glavni cilj

Omogočiti slepim in slabovidnim uporabnikom, da:
- hitro najdejo relevantne odstavke po vsebini,
- uporabljajo intuitiven način iskanja,
- preprosto vpišejo tag, npr. `#egipt #faraon`, in dobijo linke na specifične odstavke,
- dostopajo do vsebine, ki bi sicer vizualno izstopala (definicije, enačbe, posebni odstavki), preko **AI-generiranih tagov**.

---

### Install from Source

1. Clone the GitHub repository:
```sh
git clone https://github.com/makov3c/TagIT
```

2. Create and activate a virtual environment:
```sh
python3 -m venv notolog_env
source notolog_env/bin/activate  # macOS and Linux systems
notolog_env\Scripts\activate  # Windows
```

3. Install dependencies:
```sh
pip install .
```

4. Start Notolog using:
```sh
python -m notolog.app
```





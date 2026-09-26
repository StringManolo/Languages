# Languages

A personal collection of language-learning resources: interactive lessons, pronunciation guides, vocabulary references, and ready-to-import [Anki](https://apps.ankiweb.net/) decks.

Everything is published as static HTML on **GitHub Pages** and as `.apkg` files on **GitHub Releases**, so it works offline and on any device.

---

## 🌍 Languages

| Language | Lessons & Pronunciation | Anki Decks | Status |
|---|---|---|---|
| 🇷🇺 **Russian** | [Russian/](Russian/) · [Web version](https://stringmanolo.github.io/Languages/Russian/) | [Russian/Anki/](Russian/Anki/) | 🟢 Active |
| More coming… | — | — | 🔜 Planned |

> **Note:** Currently only Russian is available. Additional languages (German, Italian, Spanish, Chinese…) will be added over time using the same structure.

---

## 📖 How the repo is organized

Each language lives in its own folder and follows the same layout:

```
Languages/
├── README.md              ← you are here
└── <Language>/
    ├── README.md          ← full written guide (grammar, vocab, pronunciation)
    ├── index.html         ← interactive GitHub Pages version
    ├── alphabet.html      ← interactive alphabet
    ├── exercises.html     ← practice exercises
    ├── audio/             ← MP3 files (TTS + native recordings)
    └── Anki/              ← Anki decks + generator scripts
        ├── README.md      ← deck descriptions and download links
        └── scripts/       ← Python scripts used to build the decks
```

---

## 🇷🇺 Russian

The Russian section is the most developed so far. It includes:

### 📘 Written guide — [`Russian/README.md`](Russian/README.md)

A complete beginner-to-A1 reference covering:

- The **Cyrillic alphabet** with English sound approximations
- **Pronunciation rules** (hard vs. soft vowels, consonant exceptions, vowel reduction)
- **Greetings, farewells, apologies** (formal and informal)
- **Core vocabulary** — drinks, food, family, places
- **Pronouns**, **numbers**, **gender of nouns**, and more

### 🌐 Interactive web version

Open the live version on GitHub Pages: **[stringmanolo.github.io/Languages/Russian](https://stringmanolo.github.io/Languages/Russian/)**

- [`alphabet.html`](Russian/alphabet.html) — click each letter to hear it
- [`exercises.html`](Russian/exercises.html) — interactive practice
- [`index.html`](Russian/index.html) — full lesson index

### 🎴 Anki decks — [`Russian/Anki/`](Russian/Anki/)

Ready-to-import `.apkg` decks for spaced repetition. See the **[Anki README](Russian/Anki/)** for the full list, descriptions, credits, and direct download links.

Highlights:

- **A0** — starter phrases from YouTube *(work in progress)*
- **A1** — 200 sentences + 800 words with **real neural audio**
- **Basic** — core vocabulary from this repo
- **Core5000** — 5,000 most frequent Russian words *(third-party)*
- **LingoLlama** — 253 beginner sentences with audio *(third-party)*
- **Numbers** — 0 to 1,000,000,000, skipping predictable combinations

> All decks are compatible with **Anki Desktop**, **AnkiDroid** (Android), and **AnkiMobile** (iOS).

---

## 🚀 Quick start

### Read the lessons online

👉 **[Open the Russian course](https://stringmanolo.github.io/Languages/Russian/)**

### Clone the repo for offline use

```bash
git clone https://github.com/StringManolo/Languages.git
cd Languages
```

Then open any `index.html` in your browser, or read the `README.md` files directly.

### Get the Anki decks

Download them from the **[`anki_russian_decks` release](https://github.com/StringManolo/Languages/releases/tag/anki_russian_decks)** — or head to [`Russian/Anki/`](Russian/Anki/) for descriptions and direct links.

---

## 🛠️ Tools used

- **HTML + CSS + vanilla JS** for the interactive pages (no build step).
- **[edge-tts](https://github.com/rany2/edge-tts)** for high-quality neural Russian audio (`ru-RU-SvetlanaNeural`).
- **[genanki](https://github.com/kerrickstaley/genanki)** for programmatically building `.apkg` files.
- **GitHub Pages** for hosting the web version.
- **GitHub Releases** for hosting large `.apkg` files (not stored in Git).

---

## 🤝 Contributing

Suggestions, corrections, and new decks are welcome.

- Found a typo or a wrong translation? → [Open an issue](https://github.com/StringManolo/Languages/issues)
- Want to add a new language? → Fork the repo and follow the same folder structure, then submit a PR.
- Want to improve the Anki decks? → See the scripts in each `Anki/scripts/` folder.

---

## 📜 License

- **Original content** (lessons, HTML, scripts, original decks): [MIT License](LICENSE).
- **Third-party Anki decks** (Core5000, LingoLlama): see credits in [`Russian/Anki/`](Russian/Anki/) — each deck keeps its original author's terms.

---

## ⭐ Credits

- Thanks to the **Anki** community and to the authors of the third-party decks included here.
- Thanks to **Microsoft Edge TTS** for the free neural voices that make the audio possible.

---

## 🔗 Links

- 🏠 **Repo:** [github.com/StringManolo/Languages](https://github.com/StringManolo/Languages)
- 📚 **Russian course:** [stringmanolo.github.io/Languages/Russian](https://stringmanolo.github.io/Languages/Russian/)
- 🎴 **Anki decks:** [`anki_russian_decks` release](https://github.com/StringManolo/Languages/releases/tag/anki_russian_decks)
- 🐛 **Issues:** [github.com/StringManolo/Languages/issues](https://github.com/StringManolo/Languages/issues)


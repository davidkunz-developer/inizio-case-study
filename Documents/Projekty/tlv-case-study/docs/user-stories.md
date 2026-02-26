# Uživatelské příběhy (User Stories)

## Epics
1. **Správa a přehled vozidel:** Jako fleet manager chci vidět všechna svá přidělená vozidla, abych mohl provádět konkrétní analýzy.
2. **Kniha jízd a vytíženost:** Jako fleet manager chci analyzovat reálné jízdy a celkový nájezd kilometrů, abych věděl, jestli se vozy vyplatí.
3. **Eco-driving a bezpečnost:** Jako manager chci detekovat nevhodné chování na silnici za účelem prevence nehod a zvýšení životnosti vozů.

## User Stories

### US1: Zobrazení skupin a flotily
- **Jako** fleet manager
- **chci** na domovské obrazovce aplikace vidět seznam mých skupin a vozidel
- **abych** si mohl jednoduše naklikat konkrétní vůz, který chci prozkoumat.
- **Akceptační kritéria:**
  - Systém dotáhne data o skupinách.
  - Lze si zvolit skupinu, čímž se rozbalí/zobrazí vozový park dané skupiny s informativními štítky (SPZ, základní staty).

### US2: Přehledná Kniha Jízd
- **Jako** fleet manager
- **chci** mít u konkrétního vybraného vozidla možnost zobrazit tabulku historie jeho cest za uplynulý týden/měsíc...
- **abych** měl v ruce tvrdá data o jeho pohybu a nájezdu.
- **Akceptační kritéria:**
  - Nad výběrem vozidla funguje date-picker (od - do).
  - Objeví se tabulka (Log Book), kde řádky představují jednotlivé jízdy a obsahují hodnoty: Třída cesty, Start, Konec, Celková Vzdálenost, Prům. Rychlost.

### US3: Grafická Vizualizace vytížení
- **Jako** analytik
- **chci** vizuálně přitažlivý graf objemu naježděných kilometrů rozpadnutý po dnech
- **abych** bez dlouhého zkoumání tabulky okamžitě pochopil distribuci vytížení v čase.
- **Akceptační kritéria:**
  - Bar chart nebo line chart ukazující kilometry na denní bázi pro vybrané vozidlo.
  - Graf reaguje na zvolené datum.

### US4: Analýza Eco-driving událostí
- **Jako** fleet manager dbající na snižování nákladů a udržitelnost
- **chci** vidět záznamy o prudkém brzdění, nevybíravém zrychlování či agresivním zatáčení
- **abych** s odpovědným řidičem mohl jeho styl řízení probrat.
- **Akceptační kritéria:**
  - Widget zobrazující četnost nežádoucích událostí (Eco Driving events z API).
  - Přehled typů těchto prohřešků a jejich "Severity" (nízká, případně vyšší míra rizika).

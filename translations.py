"""
translations.py
---------------
All UI strings for the Chess Tournament Manager.
Supported languages: English (en), Nederlands (nl), Deutsch (de)
"""

TRANSLATIONS = {
    "en": {
        # Sidebar
        "app_title":         "♟ Tournament Manager",
        "round_label":       "Round",
        "players_label":     "Players",
        "nav_setup":         "🏆 Tournament Setup",
        "nav_players":       "👥 Players",
        "nav_rounds":        "⚔️ Rounds & Pairings",
        "nav_results":       "📝 Results",
        "nav_standings":     "📊 Standings",
        "create_first":      "Please create a tournament first.",

        # Setup page
        "setup_title":       "♟ Chess Tournament Manager",
        "setup_subtitle":    "Swiss System — Tournament Setup",
        "tournament_id":     "Tournament ID",
        "tournament_name":   "Tournament Name",
        "club_name":         "Club Name",
        "create_btn":        "🏆 Create Tournament",
        "fill_all_fields":   "Please fill in all fields.",
        "tournament_created":"Tournament **{name}** has been created!",
        "active_tournament": "✅ Active tournament: **{name}**",

        # Players page
        "players_title":     "👥 Player Management",
        "add_player":        "Add Player",
        "player_name":       "Name",
        "player_name_ph":    "e.g. Anna Müller",
        "player_rating":     "Rating (Elo)",
        "add_btn":           "➕ Add Player",
        "name_empty":        "Name cannot be empty.",
        "player_added":      "**{name}** added!",
        "player_list":       "Player List · {count} Players",
        "no_players":        "No players added yet.",

        # Rounds page
        "rounds_title":      "⚔️ Rounds & Pairings",
        "min_players":       "At least 2 players required.",
        "new_round":         "Start New Round",
        "round_num":         "**Round {n}**",
        "bye_label":         "Players with bye (absent)",
        "start_round_btn":   "🚀 Start Round & Generate Pairings",
        "round_started":     "Round {n} started with {count} games!",
        "view_pairings":     "View Pairings",
        "select_round":      "Select Round",
        "round_x":           "Round {n}",
        "no_rounds":         "No rounds started yet.",
        "wins":              "🏆 {name} wins",
        "draw":              "Draw",
        "open":              "Open",

        # Results page
        "results_title":     "📝 Enter Results",
        "no_rounds_yet":     "No rounds started yet.",
        "open_games":        "Open Games ({count})",
        "result_label":      "Result",
        "choose":            "— choose —",
        "white_wins":        "⬜ {name} wins",
        "black_wins":        "⬛ {name} wins",
        "draw_half":         "½ Draw",
        "notes_label":       "Note (optional)",
        "save_btn":          "✔ Save",
        "choose_result":     "Please select a result.",
        "result_saved":      "Result saved!",
        "all_done":          "✅ All games in this round have been entered.",
        "done_games":        "Completed Games ({count})",

        # Standings page
        "standings_title":   "📊 Standings",
        "metric_players":    "Players",
        "metric_rounds":     "Rounds Played",
        "metric_games":      "Total Games",
        "metric_results":    "Results Entered",
        "col_rank":          "#",
        "col_player":        "Player",
        "col_points":        "Pts",
        "col_wins":          "W",
        "col_draws":         "D",
        "col_losses":        "L",
        "col_rating":        "Elo",
        "no_standings":      "No players or results yet.",
    },

    "nl": {
        # Sidebar
        "app_title":         "♟ Toernooi Manager",
        "round_label":       "Ronde",
        "players_label":     "Spelers",
        "nav_setup":         "🏆 Toernooi Setup",
        "nav_players":       "👥 Spelers",
        "nav_rounds":        "⚔️ Rondes & Loting",
        "nav_results":       "📝 Resultaten",
        "nav_standings":     "📊 Klassement",
        "create_first":      "Maak eerst een toernooi aan.",

        # Setup page
        "setup_title":       "♟ Schaaktoernooi Manager",
        "setup_subtitle":    "Zwitsers Systeem — Toernooi Setup",
        "tournament_id":     "Toernooi-ID",
        "tournament_name":   "Toernooinama",
        "club_name":         "Clubnaam",
        "create_btn":        "🏆 Toernooi aanmaken",
        "fill_all_fields":   "Vul alle velden in.",
        "tournament_created":"Toernooi **{name}** is aangemaakt!",
        "active_tournament": "✅ Actief toernooi: **{name}**",

        # Players page
        "players_title":     "👥 Spelerbeheer",
        "add_player":        "Speler toevoegen",
        "player_name":       "Naam",
        "player_name_ph":    "bijv. Jan de Vries",
        "player_rating":     "Rating (Elo)",
        "add_btn":           "➕ Toevoegen",
        "name_empty":        "Naam mag niet leeg zijn.",
        "player_added":      "**{name}** toegevoegd!",
        "player_list":       "Spelerslijst · {count} Spelers",
        "no_players":        "Nog geen spelers toegevoegd.",

        # Rounds page
        "rounds_title":      "⚔️ Rondes & Loting",
        "min_players":       "Minimaal 2 spelers vereist.",
        "new_round":         "Nieuwe ronde starten",
        "round_num":         "**Ronde {n}**",
        "bye_label":         "Spelers met vrijloting (afwezig)",
        "start_round_btn":   "🚀 Ronde starten & Loting genereren",
        "round_started":     "Ronde {n} gestart met {count} partijen!",
        "view_pairings":     "Loting bekijken",
        "select_round":      "Ronde kiezen",
        "round_x":           "Ronde {n}",
        "no_rounds":         "Nog geen rondes gestart.",
        "wins":              "🏆 {name} wint",
        "draw":              "Remise",
        "open":              "Open",

        # Results page
        "results_title":     "📝 Resultaten invoeren",
        "no_rounds_yet":     "Nog geen rondes gestart.",
        "open_games":        "Openstaande partijen ({count})",
        "result_label":      "Resultaat",
        "choose":            "— kies —",
        "white_wins":        "⬜ {name} wint",
        "black_wins":        "⬛ {name} wint",
        "draw_half":         "½ Remise",
        "notes_label":       "Notitie (optioneel)",
        "save_btn":          "✔ Opslaan",
        "choose_result":     "Selecteer een resultaat.",
        "result_saved":      "Resultaat opgeslagen!",
        "all_done":          "✅ Alle partijen van deze ronde zijn ingevoerd.",
        "done_games":        "Afgeronde partijen ({count})",

        # Standings page
        "standings_title":   "📊 Klassement",
        "metric_players":    "Spelers",
        "metric_rounds":     "Rondes gespeeld",
        "metric_games":      "Totaal partijen",
        "metric_results":    "Resultaten ingevoerd",
        "col_rank":          "#",
        "col_player":        "Speler",
        "col_points":        "Ptn",
        "col_wins":          "W",
        "col_draws":         "R",
        "col_losses":        "V",
        "col_rating":        "Elo",
        "no_standings":      "Nog geen spelers of resultaten.",
    },

    "de": {
        # Sidebar
        "app_title":         "♟ Turnier Manager",
        "round_label":       "Runde",
        "players_label":     "Spieler",
        "nav_setup":         "🏆 Turnier Setup",
        "nav_players":       "👥 Spieler",
        "nav_rounds":        "⚔️ Runden & Paarungen",
        "nav_results":       "📝 Ergebnisse",
        "nav_standings":     "📊 Tabelle",
        "create_first":      "Bitte zuerst ein Turnier erstellen.",

        # Setup page
        "setup_title":       "♟ Schachturnier Manager",
        "setup_subtitle":    "Schweizer System — Turnier Setup",
        "tournament_id":     "Turnier-ID",
        "tournament_name":   "Turniername",
        "club_name":         "Vereinsname",
        "create_btn":        "🏆 Turnier erstellen",
        "fill_all_fields":   "Bitte alle Felder ausfüllen.",
        "tournament_created":"Turnier **{name}** wurde erstellt!",
        "active_tournament": "✅ Aktives Turnier: **{name}**",

        # Players page
        "players_title":     "👥 Spielerverwaltung",
        "add_player":        "Spieler hinzufügen",
        "player_name":       "Name",
        "player_name_ph":    "z.B. Anna Müller",
        "player_rating":     "DWZ / Elo",
        "add_btn":           "➕ Hinzufügen",
        "name_empty":        "Name darf nicht leer sein.",
        "player_added":      "**{name}** hinzugefügt!",
        "player_list":       "Spielerliste · {count} Spieler",
        "no_players":        "Noch keine Spieler hinzugefügt.",

        # Rounds page
        "rounds_title":      "⚔️ Runden & Paarungen",
        "min_players":       "Mindestens 2 Spieler erforderlich.",
        "new_round":         "Neue Runde starten",
        "round_num":         "**Runde {n}**",
        "bye_label":         "Spieler mit Freilos (absent)",
        "start_round_btn":   "🚀 Runde starten & Paarungen generieren",
        "round_started":     "Runde {n} gestartet mit {count} Partien!",
        "view_pairings":     "Paarungen anzeigen",
        "select_round":      "Runde wählen",
        "round_x":           "Runde {n}",
        "no_rounds":         "Noch keine Runden gestartet.",
        "wins":              "🏆 {name} gewinnt",
        "draw":              "Remis",
        "open":              "Offen",

        # Results page
        "results_title":     "📝 Ergebnisse eintragen",
        "no_rounds_yet":     "Noch keine Runden gestartet.",
        "open_games":        "Offene Partien ({count})",
        "result_label":      "Ergebnis",
        "choose":            "— wählen —",
        "white_wins":        "⬜ {name} gewinnt",
        "black_wins":        "⬛ {name} gewinnt",
        "draw_half":         "½ Remis",
        "notes_label":       "Notiz (optional)",
        "save_btn":          "✔ Speichern",
        "choose_result":     "Bitte ein Ergebnis wählen.",
        "result_saved":      "Ergebnis gespeichert!",
        "all_done":          "✅ Alle Partien dieser Runde wurden eingetragen.",
        "done_games":        "Abgeschlossene Partien ({count})",

        # Standings page
        "standings_title":   "📊 Turnierstand",
        "metric_players":    "Spieler",
        "metric_rounds":     "Runden gespielt",
        "metric_games":      "Partien total",
        "metric_results":    "Ergebnisse",
        "col_rank":          "#",
        "col_player":        "Spieler",
        "col_points":        "Pkt",
        "col_wins":          "S",
        "col_draws":         "R",
        "col_losses":        "N",
        "col_rating":        "Elo",
        "no_standings":      "Noch keine Spieler oder Ergebnisse vorhanden.",
    },
}


def get_text(lang: str, key: str, **kwargs) -> str:
    """Get a translated string, with optional format variables."""
    text = TRANSLATIONS.get(lang, TRANSLATIONS["en"]).get(key, key)
    return text.format(**kwargs) if kwargs else text
"""
Chess Tournament Manager - Streamlit UI
Shahmata Schaakvereniging Edition
----------------------------------------
Requires: tournament_manager.py + translations.py in the same folder!

Install & run:
    pip3 install streamlit
    python3 -m streamlit run tournament_app.py
"""

import streamlit as st
import os
import pickle
from datetime import datetime

from tournament_manager import SwissTournament, GameResult, Player, PlayerStats
from translations import get_text, TRANSLATIONS

# ─────────────────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Shahmata Tournament Manager",
    page_icon="♟",
    layout="wide"
)

# ─────────────────────────────────────────────────────────────────────────────
# PERSISTENCE  (saves to tournament_save.pkl next to the script)
# ─────────────────────────────────────────────────────────────────────────────
SAVE_FILE = "tournament_save.pkl"

def save_state():
    """Persist the full session to disk so a browser refresh restores it."""
    with open(SAVE_FILE, "wb") as f:
        pickle.dump({
            "tournament":     st.session_state.tournament,
            "player_counter": st.session_state.player_counter,
            "lang":           st.session_state.lang,
            "page":           st.session_state.page,
        }, f)

def load_state():
    """Load persisted session from disk if it exists."""
    if os.path.exists(SAVE_FILE):
        try:
            with open(SAVE_FILE, "rb") as f:
                data = pickle.load(f)
            st.session_state.tournament     = data.get("tournament")
            st.session_state.player_counter = data.get("player_counter", 1)
            st.session_state.lang           = data.get("lang", "en")
            st.session_state.page           = data.get("page", "setup")
        except Exception:
            pass  # corrupt file, start fresh

# ─────────────────────────────────────────────────────────────────────────────
# CSS  (Shahmata green/black palette)
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=Source+Sans+3:wght@400;600&display=swap');

html, body, [class*="css"] { font-family: 'Source Sans 3', sans-serif; }
h1, h2, h3 { font-family: 'Playfair Display', serif; }

.stApp { background: #0d0d0d; color: #f0f0f0; }
.block-container { padding-top: 2rem; }

.metric-card {
    background: #1a1a1a;
    border: 1px solid rgba(46,125,50,0.5);
    border-top: 3px solid #2e7d32;
    border-radius: 8px;
    padding: 1.2rem;
    text-align: center;
}
.metric-value {
    font-family: 'Playfair Display', serif;
    font-size: 2.5rem;
    color: #43a047;
    line-height: 1;
}
.metric-label {
    font-size: 0.75rem;
    color: #9e9e9e;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    margin-top: 0.4rem;
}
.player-row {
    background: #1a1a1a;
    border-left: 4px solid #2e7d32;
    padding: 0.6rem 1rem;
    margin-bottom: 0.4rem;
    border-radius: 0 6px 6px 0;
}
.game-card {
    background: #1a1a1a;
    border: 1px solid #2a2a2a;
    border-radius: 8px;
    padding: 1rem;
    margin-bottom: 0.6rem;
}
.badge-win  { background:#1b3a1c; color:#66bb6a; padding:3px 10px; border-radius:4px; font-size:0.8rem; font-weight:600; }
.badge-draw { background:#2a2a1a; color:#ffc107; padding:3px 10px; border-radius:4px; font-size:0.8rem; font-weight:600; }
.badge-open { background:#1a1a2e; color:#90caf9; padding:3px 10px; border-radius:4px; font-size:0.8rem; font-weight:600; }

div[data-testid="stSidebar"] {
    background: #111111;
    border-right: 1px solid rgba(46,125,50,0.3);
}
.stButton > button {
    background: linear-gradient(135deg, #1b5e20, #2e7d32);
    color: #ffffff;
    border: none;
    font-weight: 600;
    border-radius: 6px;
    transition: opacity 0.2s;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #2e7d32, #43a047) !important;
    color: #ffffff !important;
}
.stTextInput > div > div > input,
.stNumberInput > div > div > input {
    background: #1a1a1a !important;
    border: 1px solid rgba(46,125,50,0.4) !important;
    color: #f0f0f0 !important;
    border-radius: 6px !important;
}
.stSelectbox > div > div {
    background: #1a1a1a !important;
    border: 1px solid rgba(46,125,50,0.4) !important;
    color: #f0f0f0 !important;
    border-radius: 6px !important;
}
details {
    background: #1a1a1a !important;
    border: 1px solid #2a2a2a !important;
    border-radius: 8px !important;
}
.rank-1 { color: #43a047; font-weight: 700; font-size: 1.1rem; }
.rank-2 { color: #66bb6a; font-weight: 700; }
.rank-3 { color: #81c784; font-weight: 700; }
hr { border-color: rgba(46,125,50,0.25); }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# SESSION STATE  (load from disk on first run)
# ─────────────────────────────────────────────────────────────────────────────
if "_loaded" not in st.session_state:
    st.session_state._loaded = True
    load_state()

if "tournament"     not in st.session_state: st.session_state.tournament     = None
if "page"           not in st.session_state: st.session_state.page           = "setup"
if "player_counter" not in st.session_state: st.session_state.player_counter = 1
if "lang"           not in st.session_state: st.session_state.lang           = "en"


def t() -> SwissTournament:
    return st.session_state.tournament

def _(key: str, **kwargs) -> str:
    return get_text(st.session_state.lang, key, **kwargs)


# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='padding: 0.5rem 0 1rem 0'>
        <div style='font-family: Playfair Display, serif; font-size: 1.4rem; font-weight:900;'>
            shah<span style='color:#2e7d32'>♛</span>mata
        </div>
        <div style='font-size:0.65rem; color:#9e9e9e; letter-spacing:0.2em; text-transform:uppercase;'>
            Schaakvereniging · sinds 1970
        </div>
    </div>
    """, unsafe_allow_html=True)

    lang_options = {"en": "🇬🇧 English", "nl": "🇳🇱 Nederlands", "de": "🇩🇪 Deutsch"}
    selected_lang = st.selectbox(
        "Language / Taal / Sprache",
        options=list(lang_options.keys()),
        format_func=lambda k: lang_options[k],
        index=list(lang_options.keys()).index(st.session_state.lang)
    )
    if selected_lang != st.session_state.lang:
        st.session_state.lang = selected_lang
        save_state()
        st.rerun()

    st.markdown("---")

    if st.session_state.tournament is None:
        st.info(_("create_first"))
    else:
        st.markdown(f"**{t().name}**")
        st.markdown(f"<span style='color:#9e9e9e'>{t().club_name}</span>", unsafe_allow_html=True)
        st.markdown(
            f"<span style='color:#43a047'>⬤</span> {_('round_label')} **{t().current_round}** · "
            f"**{len(t().players)}** {_('players_label')}",
            unsafe_allow_html=True
        )
        st.markdown("---")

    pages = {
        _("nav_setup"):     "setup",
        _("nav_players"):   "players",
        _("nav_rounds"):    "rounds",
        _("nav_results"):   "results",
        _("nav_standings"): "standings",
    }
    for label, key in pages.items():
        if st.button(label, use_container_width=True):
            st.session_state.page = key
            save_state()

    # Reset button
    st.markdown("---")
    if st.button("🗑 Reset Tournament", use_container_width=True):
        if os.path.exists(SAVE_FILE):
            os.remove(SAVE_FILE)
        st.session_state.tournament     = None
        st.session_state.player_counter = 1
        st.session_state.page           = "setup"
        st.rerun()

page = st.session_state.page


# ═════════════════════════════════════════════════════════════════════════════
# PAGE: SETUP
# ═════════════════════════════════════════════════════════════════════════════
if page == "setup":
    st.markdown(f"# {_('setup_title')}")
    st.markdown(f"<span style='color:#9e9e9e'>{_('setup_subtitle')}</span>", unsafe_allow_html=True)
    st.markdown("---")

    with st.form("setup_form"):
        col1, col2, col3 = st.columns(3)
        with col1: t_id   = st.text_input(_("tournament_id"),   value="SHAHMATA2024")
        with col2: t_name = st.text_input(_("tournament_name"), value="Shahmata Club Championship")
        with col3: t_club = st.text_input(_("club_name"),        value="Shahmata")

        if st.form_submit_button(_("create_btn"), use_container_width=True):
            if not t_id or not t_name or not t_club:
                st.error(_("fill_all_fields"))
            else:
                st.session_state.tournament = SwissTournament(t_id, t_name, t_club)
                st.session_state.page = "players"
                save_state()
                st.success(_("tournament_created", name=t_name))
                st.rerun()

    if st.session_state.tournament:
        st.markdown("---")
        st.success(_("active_tournament", name=t().name))


# ═════════════════════════════════════════════════════════════════════════════
# PAGE: PLAYERS
# ═════════════════════════════════════════════════════════════════════════════
elif page == "players":
    if not st.session_state.tournament:
        st.warning(_("create_first")); st.stop()

    st.markdown(f"# {_('players_title')}")
    st.markdown("---")

    col_form, col_list = st.columns([1, 1.5])

    with col_form:
        st.markdown(f"### {_('add_player')}")
        # NOTE: clear_on_submit=False so rating value is not reset before we read it
        with st.form("add_player_form", clear_on_submit=False):
            name   = st.text_input(_("player_name"), placeholder=_("player_name_ph"), key="new_player_name")
            rating = st.number_input(_("player_rating"), min_value=100, max_value=3000, value=1500, step=10, key="new_player_rating")

            if st.form_submit_button(_("add_btn"), use_container_width=True):
                # Read from session_state keys — guaranteed correct before any reset
                actual_name   = st.session_state.get("new_player_name", "")
                actual_rating = st.session_state.get("new_player_rating", 1500)
                if not actual_name:
                    st.error(_("name_empty"))
                else:
                    pid = f"p{st.session_state.player_counter}"
                    st.session_state.player_counter += 1
                    try:
                        t().add_player(pid, actual_name, actual_rating)
                        save_state()
                        st.success(_("player_added", name=actual_name))
                    except ValueError as e:
                        st.error(str(e))

    with col_list:
        st.markdown(f"### {_('player_list', count=len(t().players))}")
        if not t().players:
            st.info(_("no_players"))
        else:
            for p in sorted(t().players.values(), key=lambda p: -p.rating):
                col_a, col_b = st.columns([4, 1])
                with col_a:
                    st.markdown(
                        f'<div class="player-row">♟ <b>{p.name}</b> &nbsp;·&nbsp; '
                        f'<span style="color:#43a047">Elo {p.rating}</span> '
                        f'<span style="color:#555; font-size:0.8em">({p.player_id})</span></div>',
                        unsafe_allow_html=True
                    )
                with col_b:
                    if st.button("✕", key=f"del_{p.player_id}"):
                        t().remove_player(p.player_id)
                        save_state()
                        st.rerun()


# ═════════════════════════════════════════════════════════════════════════════
# PAGE: ROUNDS & PAIRINGS
# ═════════════════════════════════════════════════════════════════════════════
elif page == "rounds":
    if not st.session_state.tournament:
        st.warning(_("create_first")); st.stop()

    st.markdown(f"# {_('rounds_title')}")
    st.markdown("---")

    if len(t().players) < 2:
        st.warning(_("min_players")); st.stop()

    col_new, col_view = st.columns([1, 1.5])

    with col_new:
        st.markdown(f"### {_('new_round')}")
        next_round = t().current_round + 1

        with st.form("round_form"):
            st.markdown(_("round_num", n=next_round))
            bye_options   = {p.player_id: p.name for p in t().players.values()}
            selected_byes = st.multiselect(
                _("bye_label"),
                options=list(bye_options.keys()),
                format_func=lambda pid: bye_options[pid]
            )
            if st.form_submit_button(_("start_round_btn"), use_container_width=True):
                # Guard: block new round while current round has open games
                if t().current_round > 0:
                    open_games = [
                        g for g in t().get_round_games(t().current_round)
                        if g.result is None
                    ]
                    if open_games:
                        st.error(
                            f"Round {t().current_round} still has "
                            f"{len(open_games)} unfinished game(s). "
                            f"Record all results before starting round {next_round}."
                        )
                        st.stop()
                try:
                    t().start_round(next_round)
                    pairings = t().generate_pairings(next_round, byes=selected_byes.copy())
                    t().create_games(next_round, pairings)
                    for pid in selected_byes:
                        t().record_bye(pid, next_round, score=0.0)
                    save_state()
                    st.success(_("round_started", n=next_round, count=len(pairings)))
                    st.rerun()
                except ValueError as e:
                    st.error(str(e))

    with col_view:
        st.markdown(f"### {_('view_pairings')}")
        if not t().rounds:
            st.info(_("no_rounds"))
        else:
            round_nums     = sorted(t().rounds.keys(), reverse=True)
            selected_round = st.selectbox(
                _("select_round"), round_nums,
                format_func=lambda r: _("round_x", n=r)
            )
            for game in t().get_round_games(selected_round):
                if game.result == GameResult.WHITE_WIN:
                    result_display, badge = _("wins", name=game.white_player.name), "badge-win"
                elif game.result == GameResult.BLACK_WIN:
                    result_display, badge = _("wins", name=game.black_player.name), "badge-win"
                elif game.result == GameResult.DRAW:
                    result_display, badge = _("draw"), "badge-draw"
                else:
                    result_display, badge = _("open"), "badge-open"

                st.markdown(f"""
                <div class="game-card">
                    <span style="color:#43a047;font-size:0.75em;text-transform:uppercase;letter-spacing:0.1em">
                        {game.game_id}
                    </span><br>
                    ⬜ <b>{game.white_player.name}</b> ({game.white_player.rating})
                    &nbsp;vs&nbsp;
                    ⬛ <b>{game.black_player.name}</b> ({game.black_player.rating})<br>
                    <span class="{badge}">{result_display}</span>
                </div>
                """, unsafe_allow_html=True)


# ═════════════════════════════════════════════════════════════════════════════
# PAGE: RESULTS
# ═════════════════════════════════════════════════════════════════════════════
elif page == "results":
    if not st.session_state.tournament:
        st.warning(_("create_first")); st.stop()

    st.markdown(f"# {_('results_title')}")
    st.markdown("---")

    if not t().rounds:
        st.info(_("no_rounds_yet")); st.stop()

    round_nums     = sorted(t().rounds.keys(), reverse=True)
    selected_round = st.selectbox(
        _("select_round"), round_nums,
        format_func=lambda r: _("round_x", n=r)
    )
    games      = t().get_round_games(selected_round)
    open_games = [g for g in games if g.result is None]
    done_games = [g for g in games if g.result is not None]

    if open_games:
        st.markdown(f"### {_('open_games', count=len(open_games))}")
        for game in open_games:
            white_wins_label = _("white_wins", name=game.white_player.name)
            black_wins_label = _("black_wins", name=game.black_player.name)
            draw_label       = _("draw_half")

            with st.expander(f"⚔️ {game.white_player.name} vs {game.black_player.name}", expanded=True):
                col_r, col_n, col_b = st.columns([2, 2, 1])
                with col_r:
                    result_choice = st.selectbox(
                        _("result_label"),
                        [_("choose"), white_wins_label, black_wins_label, draw_label],
                        key=f"res_{game.game_id}"
                    )
                with col_n:
                    notes = st.text_input(_("notes_label"), key=f"note_{game.game_id}")
                with col_b:
                    st.markdown("<br>", unsafe_allow_html=True)
                    if st.button(_("save_btn"), key=f"save_{game.game_id}"):
                        result_map = {
                            white_wins_label: GameResult.WHITE_WIN,
                            black_wins_label: GameResult.BLACK_WIN,
                            draw_label:       GameResult.DRAW,
                        }
                        if result_choice == _("choose"):
                            st.error(_("choose_result"))
                        else:
                            t().record_result(game.game_id, result_map[result_choice], notes)
                            save_state()
                            st.success(_("result_saved"))
                            st.rerun()
    else:
        st.success(_("all_done"))

    if done_games:
        st.markdown(f"### {_('done_games', count=len(done_games))}")
        for game in done_games:
            if game.result == GameResult.WHITE_WIN:
                label = _("white_wins", name=game.white_player.name)
            elif game.result == GameResult.BLACK_WIN:
                label = _("black_wins", name=game.black_player.name)
            else:
                label = _("draw_half")
            note_html = f"&nbsp;·&nbsp;<em>{game.notes}</em>" if game.notes else ""
            st.markdown(
                f'<div class="game-card">'
                f'<b>{game.white_player.name}</b> vs <b>{game.black_player.name}</b>'
                f'&nbsp;→&nbsp;<span class="badge-win">{label}</span>{note_html}'
                f'</div>',
                unsafe_allow_html=True
            )


# ═════════════════════════════════════════════════════════════════════════════
# PAGE: STANDINGS
# ═════════════════════════════════════════════════════════════════════════════
elif page == "standings":
    if not st.session_state.tournament:
        st.warning(_("create_first")); st.stop()

    st.markdown(f"# {_('standings_title')}")
    st.markdown("---")

    col1, col2, col3, col4 = st.columns(4)
    metrics = [
        (len(t().players),                                                            _("metric_players")),
        (t().current_round,                                                           _("metric_rounds")),
        (sum(len(r.games) for r in t().rounds.values()),                             _("metric_games")),
        (sum(1 for r in t().rounds.values() for g in r.games.values() if g.result), _("metric_results")),
    ]
    for col, (val, label) in zip([col1, col2, col3, col4], metrics):
        with col:
            st.markdown(
                f'<div class="metric-card">'
                f'<div class="metric-value">{val}</div>'
                f'<div class="metric-label">{label}</div>'
                f'</div>',
                unsafe_allow_html=True
            )

    st.markdown("<br>", unsafe_allow_html=True)

    standings = t().get_standings()
    if not standings:
        st.info(_("no_standings"))
    else:
        header_cols = st.columns([0.5, 2.5, 1, 1, 1, 1, 1.2])
        headers = [_("col_rank"), _("col_player"), _("col_points"),
                   _("col_wins"), _("col_draws"), _("col_losses"), _("col_rating")]
        for col, h in zip(header_cols, headers):
            col.markdown(
                f"<span style='color:#43a047;font-size:0.8em;text-transform:uppercase;letter-spacing:0.08em'>{h}</span>",
                unsafe_allow_html=True
            )
        st.markdown("<hr style='margin:4px 0 8px 0'>", unsafe_allow_html=True)

        rank_icons = {1: "🥇", 2: "🥈", 3: "🥉"}
        for rank, stats in enumerate(standings, 1):
            icon       = rank_icons.get(rank, f"{rank}.")
            rank_class = f"rank-{rank}" if rank <= 3 else ""
            cols       = st.columns([0.5, 2.5, 1, 1, 1, 1, 1.2])
            cols[0].markdown(f"<span class='{rank_class}'>{icon}</span>", unsafe_allow_html=True)
            cols[1].markdown(f"**{stats.player.name}**")
            cols[2].markdown(f"<b style='color:#43a047'>{stats.total_score}</b>", unsafe_allow_html=True)
            cols[3].markdown(f"<span style='color:#66bb6a'>{stats.wins}</span>",   unsafe_allow_html=True)
            cols[4].markdown(f"<span style='color:#ffc107'>{stats.draws}</span>",  unsafe_allow_html=True)
            cols[5].markdown(f"<span style='color:#ef5350'>{stats.losses}</span>", unsafe_allow_html=True)
            cols[6].markdown(f"{stats.player.rating}")
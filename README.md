# College Basketball Matchup Dashboard

A static GitHub Pages site for men's Division I basketball, built like the
[NBA](https://github.com/rhyman7/nba), [NFL](https://github.com/rhyman7/nfl) and
[CFB](https://github.com/rhyman7/cfb) Matchup Dashboards: same graphite look, team-color blocks and
Head to Head rank bars. It is the NBA site's code, adapted for 365 teams.

## Pages

- **Tonight's Matchups** (`index.html`): every game between two Division I teams on the day's
  slate, grouped by tip-off time, with the AP Top 25 rank before ranked teams. Filter by conference
  or to games with a ranked team. Each row has both teams (record, conference, adjusted net rating),
  the spread, the total, implied team totals, the arena and TV. B2B marks a team playing on
  consecutive days; "5d rest" a team with five or more days off. Live scores and ESPN's current
  line load in the browser. The date strip opens the last three days and the next six.
- **Matchup** (`matchup.html?game=<ESPN game id>`): the game header (line, total, implied score,
  neutral site and event, rest, altitude), Head to Head (each offense against the other defense,
  ranked out of all Division I teams), pace, form and rest, then both team cards: SRS/OSRS/DSRS/SoS,
  offense and defense dials, the top nine players by minutes (click a name for the last 10 games),
  defense against guards, forwards and centers, and the last ten games.
- **Team Ratings** (`ratings.html`): all 365 teams in one sortable table, filterable by conference
  or Top 25.
- **Compare Any Two Teams** (`compare.html?t1=DUKE&t2=UNC`).
- **How to Read Matchups** (`how-to-read.html`).

All pages read `data/data.json` and share `common.js`, `teamcolors.js`, `style.css` (the football
sites' stylesheet, unchanged) and `cbb.css` (the basketball additions, as in the NBA site's `nba.css`).

## Data

`scripts/build_data.py` downloads three files from
[sportsdataverse/hoopR-mbb-data](https://github.com/sportsdataverse/hoopR-mbb-data) (schedule, team
box scores, player box scores; no key needed) and writes `data/data.json`:

- **Division I** teams are the ones ESPN gives a conference (365 in 2026-27). Conference names and
  the AP rank come from ESPN's schedule.
- **Records** count every game. **Stats and ratings** count only games between two Division I teams,
  so wins over non-Division I schools don't pad the numbers.
- **Adjusted ratings**: a ridge regression over every Division I game at once, on points per 100
  possessions and on points (SRS). Neutral-site games carry no home court. Home court is held at
  3.5 points (5 per 100 possessions): a free estimate early in the season mistakes the weak
  opponents teams schedule at home for home court.
- **Pace** is possessions per 40 minutes. **Players**: each team's top nine by minutes, with their
  last 10 games. **Defense by position**: what opposing guards, forwards and centers score per game.
- **Schedule**: three days back and six ahead of the slate, games between two Division I teams, with
  rest, the AP ranks, conference-game flag and altitude for the high home courts.

The **Rebuild college basketball data** Action runs four times a day from November to April, checks
the build (`scripts/check_data.py`) and commits `data/` to `main`.

## Run it locally

```bash
pip install -r requirements.txt
python scripts/build_data.py        # writes data/data.json (about 30 seconds)
python scripts/check_data.py
python -m http.server 8000          # then open http://localhost:8000
```

## Not yet

Injury reports, the women's game, the NCAA tournament bracket view, and the value board's
projections (rhyman7/bb-value-board) come later.

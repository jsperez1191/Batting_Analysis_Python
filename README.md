# Batting Analysis

A Python script that explores MLB batting data (Lahman-style `Batting.csv` and `Salaries.csv`), comparing home run trends across players, teams, and eras, and evaluating hitter value relative to salary.

## What it does

1. **Load & inspect data**
   Reads `Batting.csv`, previews the first 5 rows, and filters out players with 0 at-bats to look at summary stats for active players only.

2. **Home run leaders**
   Sums home runs (`HR`) by `playerID` across the full dataset to rank all-time leaders.

3. **Babe Ruth era comparison**
   Isolates Babe Ruth's (`ruthba01`) career span (min to max `yearID`), then compares HR totals for all players active during that same window.

4. **HR trends over time**
   Aggregates total HR by year and plots it as a line chart ("Total HR per Season Over Time").

5. **Dodgers vs. league average**
   Groups HR by year + team, isolates the Dodgers (`teamID == 'LAN'`) from 2005 onward, computes the league-wide average HR per team per year, and plots both on one chart for comparison.

6. **On-Base Percentage (OBP)**
   Fills missing `BB`, `HBP`, and `SF` values with 0, then computes:

   ```
   OBP = (H + BB + HBP) / (AB + BB + HBP + SF)
   ```

7. **Merge with salary data**
   Joins the batting data with `Salaries.csv` on `playerID`, `yearID`, and `teamID`.

8. **Value analysis (OBP per dollar)**
   Filters to qualified hitters (salary > 0, OBP > 0, AB ≥ 200), computes `OBP / salary` as a rough "value" metric, and prints the top 5 most cost-efficient hitters by OBP for the 2015 season.

## Requirements

- Python 3
- `pandas`
- `numpy`
- `matplotlib`

**Note:** the paths are currently hardcoded to `/Users/juanperez/Downloads/`. Update these to wherever your CSVs live before running:

```python
batting = pd.read_csv('/Users/juanperez/Downloads/Batting.csv')
salaries = pd.read_csv('/Users/juanperez/Downloads/Salaries.csv')
```

Two matplotlib windows will pop up in sequence (HR over time, then Dodgers vs. league average) — close each to let the script continue.

## Output

- Console: head/describe previews, HR leaderboards, Ruth-era comparison, merged tables, and the top 5 OBP-per-dollar hitters for 2015 (Moneyball example).
- Two charts (displayed, not saved to disk).

## Possible next steps

- Save `salary` merge fallback logic — currently rows without a salary match are dropped implicitly via the `salary > 0` filter, silently excluding unsigned/unmatched players.
- Parameterize the team (`LAN`) and year (2015, 2005) so the script can be rerun for any team/season without editing code.
- Save the plots to `/outputs` (`plt.savefig(...)`) instead of only calling `plt.show()`.
- Guard against divide-by-zero in `OBP_per_dollar` if `salary` is ever 0 (currently filtered out, but worth an explicit check).

from pathlib import Path
import re
import folium
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import streamlit as st
from streamlit_folium import st_folium

# Set page to wide mode for a clean map layout
st.set_page_config(page_title="Website Hits Map", layout="wide")

# Determine paths relative to this script file
BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "data" / "website_hits.txt"


def parse_hits_file(filepath: Path) -> list[tuple[str, int]]:
    """Parses 'City, Country: 123' format from the file."""
    if not filepath.exists():
        return []

    records = []
    line_pattern = re.compile(r"^(.*?):\s*(\d+)")

    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("***"):
                continue

            match = line_pattern.match(line)
            if match:
                city, hits = match.groups()
                records.append((city.strip(), int(hits)))

    return records


# Cache geocoding results so reruns/reloads don't hit OSM's rate limits repeatedly
@st.cache_data(show_spinner=False)
def get_coordinates(city_name: str) -> tuple[float, float] | None:
    geolocator = Nominatim(user_agent="codespaces_website_hits_app")
    geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1.0)
    try:
        location = geocode(city_name)
        if location:
            return (location.latitude, location.longitude)
    except Exception:
        pass
    return None


# --- App UI ---
st.title("🌐 Website Hits by City")

if not DATA_FILE.exists():
    st.error(f"Could not find data file at `{DATA_FILE}`. Please ensure the `data` folder and file exist.")
    st.stop()

records = parse_hits_file(DATA_FILE)

if not records:
    st.warning("No records found in `website_hits.txt`.")
    st.stop()

# Progress tracking for the first-time geocoding pass
with st.spinner("Resolving coordinates for cities..."):
    resolved_locations = []
    for city, hits in records:
        coords = get_coordinates(city)
        if coords:
            resolved_locations.append((city, hits, coords[0], coords[1]))

# Create the Folium map
# Centered roughly on the first result, or fallback to [20, 0]
start_coords = [resolved_locations[0][2], resolved_locations[0][3]] if resolved_locations else [20, 0]
m = folium.Map(location=start_coords, zoom_start=2, tiles="CartoDB positron")

for city, hits, lat, lon in resolved_locations:
    # Clicking marker opens this popup
    popup_html = f"""
    <div style="font-family: sans-serif; font-size: 13px;">
        <h4 style="margin: 0 0 5px 0;">{city}</h4>
        <b>Avg Hits/Day:</b> {hits:,}
    </div>
    """
    folium.Marker(
        location=[lat, lon],
        tooltip=f"{city} (click to view hits)",
        popup=folium.Popup(popup_html, max_width=200),
        icon=folium.Icon(color="blue", icon="info-sign"),
    ).add_to(m)

# Render map in Streamlit
st_folium(m, width="100%", height=600)

# Optional sidebar summary table
with st.sidebar:
    st.subheader("Data Summary")
    st.write(f"Total Cities: **{len(resolved_locations)}**")
    st.dataframe(
        [{"City": c, "Hits/Day": h} for c, h, _, _ in resolved_locations],
        use_container_width=True,
    )
import streamlit as st
import pandas as pd
import sqlite3
import re
from datetime import datetime

# --- 1. COMPREHENSIVE AREA CODE MASTER LIST ---
AREA_CODE_MAP = {
    "201": "NJ", "202": "DC", "203": "CT", "205": "AL", "206": "WA", "207": "ME", "208": "ID", "209": "CA",
    "210": "TX", "212": "NY", "213": "CA", "214": "TX", "215": "PA", "216": "OH", "217": "IL", "218": "MN",
    "219": "IN", "220": "OH", "223": "PA", "224": "IL", "225": "LA", "227": "MD", "228": "MS", "229": "GA",
    "231": "MI", "234": "OH", "239": "FL", "240": "MD", "248": "MI", "251": "AL", "252": "NC", "253": "WA",
    "254": "TX", "256": "AL", "260": "IN", "262": "WI", "267": "PA", "269": "MI", "270": "KY", "272": "PA",
    "274": "WI", "276": "VA", "279": "CA", "281": "TX", "283": "OH", "301": "MD", "302": "DE", "303": "CO",
    "304": "WV", "305": "FL", "307": "WY", "308": "NE", "309": "IL", "310": "CA", "312": "IL", "313": "MI",
    "314": "MO", "315": "NY", "316": "KS", "317": "IN", "318": "LA", "319": "IA", "320": "MN", "321": "FL",
    "323": "CA", "325": "TX", "326": "OH", "327": "AR", "330": "OH", "331": "IL", "332": "NY", "334": "AL",
    "336": "NC", "337": "LA", "339": "MA", "341": "CA", "346": "TX", "347": "NY", "351": "MA", "352": "FL",
    "360": "WA", "361": "TX", "364": "KY", "380": "OH", "385": "UT", "386": "FL", "401": "RI", "402": "NE",
    "404": "GA", "405": "OK", "406": "MT", "407": "FL", "408": "CA", "409": "TX", "410": "MD", "412": "PA",
    "413": "MA", "414": "WI", "415": "CA", "417": "MO", "419": "OH", "423": "TN", "424": "CA", "425": "WA",
    "430": "TX", "432": "TX", "434": "VA", "435": "UT", "440": "OH", "442": "CA", "443": "MD", "445": "PA",
    "447": "IL", "448": "FL", "458": "OR", "463": "IN", "464": "IL", "469": "TX", "470": "GA", "475": "CT",
    "478": "GA", "479": "AR", "480": "AZ", "484": "PA", "501": "AR", "502": "KY", "503": "OR", "504": "LA",
    "505": "NM", "507": "MN", "508": "MA", "509": "WA", "510": "CA", "512": "TX", "513": "OH", "515": "IA",
    "516": "NY", "517": "MI", "518": "NY", "520": "AZ", "530": "CA", "531": "NE", "534": "WI", "539": "OK",
    "540": "VA", "541": "OR", "551": "NJ", "557": "MO", "559": "CA", "561": "FL", "562": "CA", "563": "IA",
    "564": "WA", "567": "OH", "570": "PA", "571": "VA", "572": "OK", "573": "MO", "574": "IN", "575": "NM",
    "580": "OK", "582": "PA", "585": "NY", "586": "MI", "601": "MS", "602": "AZ", "603": "NH", "605": "SD",
    "606": "KY", "607": "NY", "608": "WI", "609": "NJ", "610": "PA", "612": "MN", "614": "OH", "615": "TN",
    "616": "MI", "617": "MA", "618": "IL", "619": "CA", "620": "KS", "623": "AZ", "626": "CA", "628": "CA",
    "629": "TN", "630": "IL", "631": "NY", "636": "MO", "640": "NJ", "641": "IA", "646": "NY", "650": "CA",
    "651": "MN", "657": "CA", "659": "AL", "660": "MO", "661": "CA", "662": "MS", "667": "MD", "669": "CA",
    "678": "GA", "681": "WV", "682": "TX", "689": "FL", "701": "ND", "702": "NV", "703": "VA", "704": "NC",
    "706": "GA", "707": "CA", "708": "IL", "712": "IA", "713": "TX", "714": "CA", "715": "WI", "716": "NY",
    "717": "PA", "718": "NY", "719": "CO", "720": "CO", "724": "PA", "725": "NV", "726": "TX", "727": "FL",
    "730": "IL", "731": "TN", "732": "NJ", "734": "MI", "737": "TX", "740": "OH", "743": "NC", "747": "CA",
    "754": "FL", "757": "VA", "760": "CA", "762": "GA", "763": "MN", "765": "IN", "769": "MS", "770": "GA",
    "772": "FL", "773": "IL", "774": "MA", "775": "NV", "779": "IL", "781": "MA", "785": "KS", "786": "FL",
    "787": "PR", "801": "UT", "802": "VT", "803": "SC", "804": "VA", "805": "CA", "806": "TX", "808": "HI",
    "810": "MI", "812": "IN", "813": "FL", "814": "PA", "815": "IL", "816": "MO", "817": "TX", "818": "CA",
    "820": "CA", "821": "SC", "828": "NC", "830": "TX", "831": "CA", "832": "TX", "838": "NY", "839": "SC",
    "843": "SC", "845": "NY", "847": "IL", "848": "NJ", "850": "FL", "854": "SC", "856": "NJ", "857": "MA",
    "858": "CA", "859": "KY", "860": "CT", "862": "NJ", "863": "FL", "864": "SC", "865": "TN", "870": "AR",
    "872": "IL", "878": "PA", "901": "TN", "903": "TX", "904": "FL", "906": "MI", "907": "AK", "908": "NJ",
    "909": "CA", "910": "NC", "912": "GA", "913": "KS", "914": "NY", "915": "TX", "916": "CA", "917": "NY",
    "918": "OK", "919": "NC", "920": "WI", "925": "CA", "928": "AZ", "929": "NY", "930": "IN", "931": "TN",
    "934": "NY", "936": "TX", "937": "OH", "938": "AL", "940": "TX", "941": "FL", "945": "TX", "947": "MI",
    "948": "VA", "949": "CA", "951": "CA", "952": "MN", "954": "FL", "956": "TX", "959": "CT", "970": "CO",
    "971": "OR", "972": "TX", "973": "NJ", "975": "MO", "978": "MA", "979": "TX", "980": "NC", "984": "NC",
    "985": "LA", "986": "ID", "989": "MI"
}
TOLL_FREE = ["800", "888", "877", "866", "855", "844", "833", "883"]

# --- 2. DATABASE SETUP ---
conn = sqlite3.connect('final_master_data.db', check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS phone_data 
             (phone TEXT, state TEXT, original_state TEXT, upload_time TEXT)''')
conn.commit()

# --- 3. CLEANING ENGINE ---
def process_row(p_val, s_val, timestamp):
    p = re.sub(r'\D', '', str(p_val).split('.')[0].strip())
    if len(p) == 11 and p.startswith('1'): p = p[1:]
    orig_s = str(s_val).strip().upper()
    ac = p[:3]
    
    mapped_s = AREA_CODE_MAP.get(ac)
    if ac in TOLL_FREE: correct_s = "Toll-Free"
    elif mapped_s: correct_s = mapped_s
    elif len(orig_s) == 2 and orig_s != "UN": correct_s = orig_s
    else: correct_s = "Unknown"
    
    return p, correct_s, orig_s, timestamp

# --- 4. APP UI ---
st.set_page_config(page_title="Bulk State Manager Pro", layout="wide")

with st.sidebar:
    st.header("📂 Bulk Import")
    uploaded_files = st.file_uploader("Upload CSV files", type=['csv'], accept_multiple_files=True)
    
    if uploaded_files:
        if st.button(f"🚀 Process {len(uploaded_files)} Files"):
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            prog = st.progress(0)
            for i, f in enumerate(uploaded_files):
                df = pd.read_csv(f).iloc[:, [0, 1]]
                df.columns = ['phone', 'state']
                res = df.apply(lambda x: process_row(x['phone'], x['state'], now), axis=1)
                final = pd.DataFrame(res.tolist(), columns=['phone', 'state', 'original_state', 'upload_time'])
                final.to_sql('phone_data', conn, if_exists='append', index=False)
                prog.progress((i + 1) / len(uploaded_files))
            st.success("Batch Uploaded!")
            st.experimental_rerun()

    st.markdown("---")
    st.header("🛠️ Data Quality Tools")
    all_df = pd.read_sql("SELECT * FROM phone_data", conn)

    if not all_df.empty:
        if st.button("🔍 Find All Duplicates"):
            dupes = all_df[all_df.duplicated(subset=['phone'], keep=False)]
            st.session_state['dupe_view'] = dupes

        if st.button("✂️ Remove Duplicates"):
            clean = all_df.drop_duplicates(subset=['phone'])
            c.execute("DELETE FROM phone_data")
            clean.to_sql('phone_data', conn, if_exists='append', index=False)
            st.success("Cleaned!")
            st.experimental_rerun()

        if st.button("↩️ Undo Last Upload Batch"):
            c.execute("DELETE FROM phone_data WHERE upload_time = (SELECT MAX(upload_time) FROM phone_data)")
            conn.commit()
            st.experimental_rerun()

    with st.expander("⚠️ Danger Zone"):
        if st.button("WIPE ENTIRE DATABASE"):
            c.execute("DELETE FROM phone_data")
            conn.commit()
            st.experimental_rerun()

# --- 5. DASHBOARD ---
st.title("📊 Regional Intelligence Dashboard")

if all_df.empty:
    st.info("The database is empty. Upload CSV files to begin.")
else:
    # KPI metrics
    dupe_count = all_df.duplicated(subset=['phone']).sum()
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Records", f"{len(all_df):,}")
    m2.metric("Verified States", all_df[~all_df['state'].isin(['Unknown', 'Toll-Free'])]['state'].nunique())
    m3.metric("Duplicate Rows", f"{dupe_count:,}")
    m4.metric("Unknowns", len(all_df[all_df['state'] == 'Unknown']))

    # Duplicate Preview
    if 'dupe_view' in st.session_state and not st.session_state['dupe_view'].empty:
        with st.expander("⚠️ Reviewing Duplicates", expanded=True):
            # NO hide_index for older versions
            st.dataframe(st.session_state['dupe_view'][['phone', 'state']], use_container_width=True)
            if st.button("Close Preview"):
                del st.session_state['dupe_view']
                st.experimental_rerun()

    st.markdown("---")
    
    # State Grid
    states = sorted(all_df['state'].unique())
    cols = st.columns(10)
    for i, s in enumerate(states):
        count = len(all_df[all_df['state'] == s])
        if cols[i % 10].button(f"{s}\n({count})"):
            st.session_state['sel_s'] = s

    if 'sel_s' in st.session_state:
        sel = st.session_state['sel_s']
        res = all_df[all_df['state'] == sel][['phone', 'state']]
        st.markdown(f"### 📍 Records for {sel}")
        # NO hide_index for older versions
        st.dataframe(res, use_container_width=True)
        
        # DOWNLOAD WITHOUT INDEX
        csv = res.to_csv(index=False).encode('utf-8')
        st.download_button(f"📥 Download {sel} CSV", csv, f"{sel}_records.csv", "text/csv")
        
    st.markdown("---")
    st.subheader("📊 State Distribution")
    st.bar_chart(all_df['state'].value_counts())
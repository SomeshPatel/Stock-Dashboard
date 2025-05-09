import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.express as px
from datetime import datetime, timedelta


COLORS = {
    
    "bg_main": "#01031a",         
    "bg_sidebar": "#2c3e50",       
    "bg_card": "#2c3e50",          
    
    # Text Colors
    "text_primary": "#FFFFFF",     
    "text_secondary": "#7f8c8d",   
    
    
    "accent_primary": "#3498db",    
    "accent_success": "#27ae60",    
    "accent_danger": "#e74c3c",    
    
   
    "chart_line": "#3498db",        
    "chart_ma50": "#f39c12",       
    "chart_ma200": "#9b59b6",       
}


st.set_page_config(
    layout="wide", 
    page_title="EquityX - Stock Analysis Dashboard",
    page_icon="📈"
)

#  CSS
st.markdown(f"""
<style>
    .stApp {{
        background-color: {COLORS['bg_main']};
    }}
    [data-testid="stSidebar"] {{
        background-color: {COLORS['bg_sidebar']} !important;
    }}
    h1, h2, h3, h4, h5, h6 {{
        color: {COLORS['text_primary']};
    }}
    .stMetric {{
        background-color: {COLORS['bg_card']};
        border-radius: 8px;
        padding: 10px;
        border-left: 3px solid {COLORS['accent_primary']};
    }}
    .stDataFrame {{
        border: 1px solid rgba(255, 255, 255, 0.1);
    }}
</style>
""", unsafe_allow_html=True)


@st.cache_data
def get_indian_stocks():
    
    return {
        "RELIANCE.NS": "Reliance Industries",
        "TATASTEEL.NS": "Tata Steel",
        "HDFCBANK.NS": "HDFC Bank",
        "INFY.NS": "Infosys",
        "TCS.NS": "Tata Consultancy",
        "RELIANCE.NS": "Reliance Industries",
            "TATASTEEL.NS": "Tata Steel",
            "HDFCBANK.NS": "HDFC Bank",
            "INFY.NS": "Infosys",
            "TCS.NS": "Tata Consultancy",
            "ICICIBANK.NS": "ICICI Bank",
            "BHARTIARTL.NS": "Bharti Airtel",
            "LT.NS": "Larsen & Toubro",
            "ITC.NS": "ITC Limited",
            "SBIN.NS": "State Bank of India",
            "ASIANPAINT.NS": "Asian Paints",
            "HINDUNILVR.NS": "Hindustan Unilever",
            "KOTAKBANK.NS": "Kotak Mahindra Bank",
            "BAJFINANCE.NS": "Bajaj Finance",
            "HCLTECH.NS": "HCL Technologies",
            "WIPRO.NS": "Wipro",
            "ONGC.NS": "Oil & Natural Gas Corp",
            "NTPC.NS": "NTPC",
            "POWERGRID.NS": "Power Grid Corp",
            "SUNPHARMA.NS": "Sun Pharmaceuticals",
            "CGCL.NS": "Capri Global Capital Limited",
            "RHIM.NS": "RHI Magnesita India Limited",
            "GPPL.NS": "Gujarat Pipavav Port Limited",
            "SAPPHIRE.NS": "Sapphire Foods India Limited",
            "BSE.NS": "BSE Limited",
            "WELCORP.NS": "Welspun Corp Limited",
            "AADHARHFC.NS": "Aadhar Housing Finance Limited",
            "NH.NS": "Narayana Hrudayalaya Limited",
            "ADANIENSOL.NS": "Adani Energy Solutions Limited",
            "KIMS.NS": "Krishna Institute of Medical Sciences Limited",
            "NEWGEN.NS": "Newgen Software Technologies Limited",
            "ERIS.NS": "Eris Lifesciences Limited",
            "HUDCO.NS": "Housing & Urban Development Corporation Limited",
            "BANKBARODA.NS": "Bank of Baroda",
            "RAMCOCEM.NS": "The Ramco Cements Limited",
            "GVT&D.NS": "GVK Power & Infrastructure Limited",
            "DIXON.NS": "Dixon Technologies (India) Limited",
            "GAIL.NS": "GAIL (India) Limited",
            "MFSL.NS": "Max Financial Services Limited",
            "PERSISTENT.NS": "Persistent Systems Limited",
            "TEJASNET.NS": "Tejas Networks Limited",
            "MAPMYINDIA.NS": "CE Info Systems Limited (MapmyIndia)",
            "CONCORDBIO.NS": "Concord Biotech Limited",
            "JUBLPHARMA.NS": "Jubilant Pharmova Limited",
            "GODFRYPHLP.NS": "Godfrey Phillips India Limited",
            "MAZDOCK.NS": "Mazagon Dock Shipbuilders Limited",
            "ACE.NS": "Action Construction Equipment Limited",
            "POLICYBZR.NS": "PB Fintech Limited (Policybazaar)",
            "SUPREMEIND.NS": "Supreme Industries Limited",
            "GAEL.NS": "Gujarat Ambuja Exports Limited",
            "BAJAJFINSV.NS": "Bajaj Finserv Limited",
            "JINDALSAW.NS": "Jindal Saw Limited",
            "UNITDSPR.NS": "United Spirits Limited",
            "HEROMOTOCO.NS": "Hero MotoCorp Limited",
            "MANYAVAR.NS": "Vedant Fashions Limited (Manyavar)",
            "FSL.NS": "Firstsource Solutions Limited",
            "SPARC.NS": "Sun Pharma Advanced Research Company Limited",
            "JSWINFRA.NS": "JSW Infrastructure Limited",
            "TVSSCS.NS": "TVS Supply Chain Solutions Limited",
            "HDFCLIFE.NS": "HDFC Life Insurance Company Limited",
            "UNIONBANK.NS": "Union Bank of India",
            "HOMEFIRST.NS": "Home First Finance Company India Limited",
            "NBCC.NS": "NBCC (India) Limited",
            "JYOTICNC.NS": "Jyoti CNC Automation Limited",
            "OIL.NS": "Oil India Limited",
            "GLENMARK.NS": "Glenmark Pharmaceuticals Limited",
            "THERMAX.NS": "Thermax Limited",
            "KIRLOSBROS.NS": "Kirloskar Brothers Limited",
            "LT.NS": "Larsen & Toubro Limited",
            "GSFC.NS": "Gujarat State Fertilizers & Chemicals Limited",
            "SAREGAMA.NS": "Saregama India Limited",
            "KIRLOSENG.NS": "Kirloskar Oil Engines Limited",
            "DMART.NS": "Avenue Supermarts Limited (D-Mart)",
            "DBREALTY.NS": "D B Realty Limited",
            "TRENT.NS": "Trent Limited",
            "DEEPAKFERT.NS": "Deepak Fertilisers & Petrochemicals Corporation Limited",
            "LODHA.NS": "Macrotech Developers Limited (Lodha)",
            "ADANIGREEN.NS": "Adani Green Energy Limited",
            "ULTRACEMCO.NS": "UltraTech Cement Limited",
            "PFC.NS": "Power Finance Corporation Limited",
            "WIPRO.NS": "Wipro Limited",
            "BEML.NS": "BEML Limited",
            "PNB.NS": "Punjab National Bank",
            "CCL.NS": "CCL Products (India) Limited",
            "UTIAMC.NS": "UTI Asset Management Company Limited",
            "KEI.NS": "KEI Industries Limited",
            "ASTRAZEN.NS": "AstraZeneca Pharma India Limited",
            "SHREECEM.NS": "Shree Cement Limited",
            "CASTROLIND.NS": "Castrol India Limited",
            "JKCEMENT.NS": "JK Cement Limited",
            "EQUITASBNK.NS": "Equitas Small Finance Bank Limited",
            "UBL.NS": "United Breweries Limited",
            "SBFC.NS": "SBFC Finance Limited",
            "JKLAKSHMI.NS": "JK Lakshmi Cement Limited",
            "BPCL.NS": "Bharat Petroleum Corporation Limited",
            "WHIRLPOOL.NS": "Whirlpool of India Limited",
            "HDFCBANK.NS": "HDFC Bank Limited",
            "MARICO.NS": "Marico Limited",
            "RAINBOW.NS": "Rainbow Children's Medicare Limited",
            "ATUL.NS": "Atul Limited",
            "HINDPETRO.NS": "Hindustan Petroleum Corporation Limited",
            "MAHSEAMLES.NS": "Maharashtra Seamless Limited",
            "PIIND.NS": "PI Industries Limited",
            "FEDERALBNK.NS": "The Federal Bank Limited",
            "BALRAMCHIN.NS": "Balrampur Chini Mills Limited",
            "BHEL.NS": "Bharat Heavy Electricals Limited",
            "LLOYDSME.NS": "Lloyds Metals and Energy Limited",
            "AAVAS.NS": "Aavas Financiers Limited",
            "INDIGO.NS": "InterGlobe Aviation Limited (IndiGo)",
            "GRASIM.NS": "Grasim Industries Limited",
            "IGL.NS": "Indraprastha Gas Limited",
            "GODREJIND.NS": "Godrej Industries Limited",
            "POLYCAB.NS": "Polycab India Limited",
            "CREDITACC.NS": "CRISIL Limited",
            "GMDCLTD.NS": "Gujarat Mineral Development Corporation Limited",
            "EIHOTEL.NS": "EIH Limited",
            "CUMMINSIND.NS": "Cummins India Limited",
            "ZEEL.NS": "Zee Entertainment Enterprises Limited",
            "VINATIORGA.NS": "Vinati Organics Limited",
            "BBTC.NS": "Bombay Burmah Trading Corporation Limited",
            "HAL.NS": "Hindustan Aeronautics Limited",
            "MAHLIFE.NS": "Mahindra Lifespace Developers Limited",
            "GSPL.NS": "Gujarat State Petronet Limited",
            "HBLENGINE.NS": "HBL Power Systems Limited",
            "AMBUJACEM.NS": "Ambuja Cements Limited",
            "LICHSGFIN.NS": "LIC Housing Finance Limited",
            "ESCORTS.NS": "Escorts Kubota Limited",
            "DALBHARAT.NS": "Dalmia Bharat Limited",
            "JYOTHYLAB.NS": "Jyothy Labs Limited",
            "TATACONSUM.NS": "Tata Consumer Products Limited",
            "BAJFINANCE.NS": "Bajaj Finance Limited",
            "NCC.NS": "NCC Limited",
            "GRSE.NS": "Garden Reach Shipbuilders & Engineers Limited",
            "GNFC.NS": "Gujarat Narmada Valley Fertilizers & Chemicals Limited",
            "COALINDIA.NS": "Coal India Limited",
            "VBL.NS": "Varun Beverages Limited",
            "TATAINVEST.NS": "Tata Investment Corporation Limited",
            "PRAJIND.NS": "Praj Industries Limited",
            "NAVINFLUOR.NS": "Navin Fluorine International Limited",
            "HAVELLS.NS": "Havells India Limited",
            "IFCI.NS": "IFCI Limited",
            "REDINGTON.NS": "Redington Limited",
            "AEGISLOG.NS": "Aegis Logistics Limited",
            "COCHINSHIP.NS": "Cochin Shipyard Limited",
            "ABCAPITAL.NS": "Aditya Birla Capital Limited",
            "PNBHOUSING.NS": "PNB Housing Finance Limited",
            "GILLETTE.NS": "Gillette India Limited",
            "IREDA.NS": "Indian Renewable Energy Development Agency Limited",
            "PAYTM.NS": "One 97 Communications Limited (Paytm)",
            "LALPATHLAB.NS": "Dr. Lal PathLabs Limited",
            "CESC.NS": "CESC Limited",
            "CHOLAHLDNG.NS": "Cholamandalam Financial Holdings Limited",
            "ICICIBANK.NS": "ICICI Bank Limited",
            "BRITANNIA.NS": "Britannia Industries Limited",
            "NETWORK18.NS": "Network18 Media & Investments Limited",
            "SOLARINDS.NS": "Solar Industries India Limited",
            "MANKIND.NS": "Mankind Pharma Limited",
            "ACI.NS": "Archean Chemical Industries Limited",
            "POWERGRID.NS": "Power Grid Corporation of India Limited",
            "NESTLEIND.NS": "Nestle India Limited",
            "INDIACEM.NS": "The India Cements Limited",
            "EMAMILTD.NS": "Emami Limited",
            "MAXHEALTH.NS": "Max Healthcare Institute Limited",
            "BANKINDIA.NS": "Bank of India",
            "MOTILALOFS.NS": "Motilal Oswal Financial Services Limited",
            "JPPOWER.NS": "Jaiprakash Power Ventures Limited",
            "CUB.NS": "City Union Bank Limited",
            "RECLTD.NS": "REC Limited",
            "IRB.NS": "IRB Infrastructure Developers Limited",
            "MGL.NS": "Mahanagar Gas Limited",
            "RCF.NS": "Rashtriya Chemicals & Fertilizers Limited",
            "GUJGASLTD.NS": "Gujarat Gas Limited",
            "VEDL.NS": "Vedanta Limited",
            "TATAPOWER.NS": "Tata Power Company Limited",
            "HFCL.NS": "HFCL Limited",
            "BRIGADE.NS": "Brigade Enterprises Limited",
            "GPIL.NS": "Godawari Power & Ispat Limited",
            "JSWSTEEL.NS": "JSW Steel Limited",
            "VIPIND.NS": "VIP Industries Limited",
            "SCHNEIDER.NS": "Schneider Electric Infrastructure Limited",
            "JKTYRE.NS": "JK Tyre & Industries Limited",
            "JUBLFOOD.NS": "Jubilant FoodWorks Limited",
            "WELSPUNLIV.NS": "Welspun Living Limited",
            "BIKAJI.NS": "Bikaji Foods International Limited",
            "IEX.NS": "Indian Energy Exchange Limited",
            "NIACL.NS": "The New India Assurance Company Limited",
            "SHRIRAMFIN.NS": "Shriram Finance Limited",
            "AXISBANK.NS": "Axis Bank Limited",
            "ADANIPOWER.NS": "Adani Power Limited",
            "FINPIPE.NS": "Finolex Industries Limited",
            "CRISIL.NS": "CRISIL Limited",
            "ANANDRATHI.NS": "Anand Rathi Wealth Limited",
            "ENGINERSIN.NS": "Engineers India Limited",
            "ZFCVINDIA.NS": "ZF Commercial Vehicle Control Systems India Limited",
            "ITC.NS": "ITC Limited",
            "BEL.NS": "Bharat Electronics Limited",
            "CANBK.NS": "Canara Bank",
            "CGPOWER.NS": "CG Power and Industrial Solutions Limited",
            "FINCABLES.NS": "Finolex Cables Limited",
            "TRIDENT.NS": "Trident Limited",
            "BASF.NS": "BASF India Limited",
            "NTPC.NS": "NTPC Limited",
            "CONCOR.NS": "Container Corporation of India Limited",
            "JWL.NS": "Jupiter Wagons Limited",
            "TCS.NS": "Tata Consultancy Services Limited",
            "LEMONTREE.NS": "Lemon Tree Hotels Limited",
            "JUSTDIAL.NS": "Just Dial Limited",
            "MARUTI.NS": "Maruti Suzuki India Limited",
            "MCX.NS": "Multi Commodity Exchange of India Limited",
            "HDFCAMC.NS": "HDFC Asset Management Company Limited",
            "MMTC.NS": "MMTC Limited",
            "LATENTVIEW.NS": "Latent View Analytics Limited",
            "PNCINFRA.NS": "PNC Infratech Limited",
            "MPHASIS.NS": "Mphasis Limited",
            "TTML.NS": "Tata Teleservices (Maharashtra) Limited",
            "PEL.NS": "Piramal Enterprises Limited",
            "ABSLAMC.NS": "Aditya Birla Sun Life AMC Limited",
            "TITAN.NS": "Titan Company Limited",
            "ELGIEQUIP.NS": "Elgi Equipments Limited",
            "SBIN.NS": "State Bank of India",
            "FORTIS.NS": "Fortis Healthcare Limited",
            "TIINDIA.NS": "Tube Investments of India Limited",
            "COFORGE.NS": "Coforge Limited",
            "AMBER.NS": "Amber Enterprises India Limited",
            "LTF.NS": "L&T Finance Holdings Limited",
            "EIDPARRY.NS": "EID Parry India Limited",
            "AIAENG.NS": "AIA Engineering Limited",
            "HINDUNILVR.NS": "Hindustan Unilever Limited",
            "LTTS.NS": "L&T Technology Services Limited",
            "KEC.NS": "KEC International Limited",
            "STARHEALTH.NS": "Star Health and Allied Insurance Company Limited",
            "UPL.NS": "UPL Limited",
            "PRESTIGE.NS": "Prestige Estates Projects Limited",
            "ADANIPORTS.NS": "Adani Ports and Special Economic Zone Limited",
            "AFFLE.NS": "Affle (India) Limited",
            "SUNTV.NS": "Sun TV Network Limited",
            "ONGC.NS": "Oil and Natural Gas Corporation Limited",
            "GODREJCP.NS": "Godrej Consumer Products Limited",
            "GESHIP.NS": "The Great Eastern Shipping Company Limited",
            "INDIAMART.NS": "IndiaMART InterMESH Limited",
            "BAJAJ-AUTO.NS": "Bajaj Auto Limited",
            "DABUR.NS": "Dabur India Limited",
            "ROUTE.NS": "ROUTE Mobile Limited",
            "LICI.NS": "Life Insurance Corporation of India",
            "KAYNES.NS": "Kaynes Technology India Limited",
            "SBILIFE.NS": "SBI Life Insurance Company Limited",
            "DATAPATTNS.NS": "Data Patterns (India) Limited",
            "ICICIGI.NS": "ICICI Lombard General Insurance Company Limited",
            "IRCTC.NS": "Indian Railway Catering and Tourism Corporation Limited",
            "NLCINDIA.NS": "NLC India Limited",
            "LINDEINDIA.NS": "Linde India Limited",
            "SOBHA.NS": "Sobha Limited",
            "BDL.NS": "Bharat Dynamics Limited",
            "LTIM.NS": "L&T Infotech Limited",
            "KARURVYSYA.NS": "Karur Vysya Bank Limited",
            "HINDALCO.NS": "Hindalco Industries Limited",
            "POWERINDIA.NS": "Hitachi Energy India Limited",
            "NMDC.NS": "NMDC Limited",
            "TRIVENI.NS": "Triveni Engineering & Industries Limited",
            "METROPOLIS.NS": "Metropolis Healthcare Limited",
            "BOSCHLTD.NS": "Bosch Limited",
            "RRKABEL.NS": "RR Kabel Limited",
            "SRF.NS": "SRF Limited",
            "ATGL.NS": "Adani Total Gas Limited",
            "HSCL.NS": "Himadri Speciality Chemical Limited",
            "ACC.NS": "ACC Limited",
            "RTNINDIA.NS": "RattanIndia Power Limited",
            "TATACHEM.NS": "Tata Chemicals Limited",
            "RELIANCE.NS": "Reliance Industries Limited",
            "SBICARD.NS": "SBI Cards and Payment Services Limited",
            "J&KBANK.NS": "The Jammu & Kashmir Bank Limited",
            "3MINDIA.NS": "3M India Limited",
            "AARTIIND.NS": "Aarti Industries Limited",
            "OBEROIRLTY.NS": "Oberoi Realty Limited",
            "APLAPOLLO.NS": "APL Apollo Tubes Limited",
            "ABBOTINDIA.NS": "Abbott India Limited",
            "SAIL.NS": "Steel Authority of India Limited",
            "BLUESTARCO.NS": "Blue Star Limited",
            "APTUS.NS": "Aptus Value Housing Finance India Limited",
            "JIOFIN.NS": "Jio Financial Services Limited",
            "UCOBANK.NS": "UCO Bank",
            "INFY.NS": "Infosys Limited",
            "TECHM.NS": "Tech Mahindra Limited",
            "IRCON.NS": "IRCON International Limited",
            "CHAMBLFERT.NS": "Chambal Fertilizers & Chemicals Limited",
            "OFSS.NS": "Oracle Financial Services Software Limited",
            "ASIANPAINT.NS": "Asian Paints Limited",
            "SWSOLAR.NS": "Sterling and Wilson Renewable Energy Limited",
            "JINDALSTEL.NS": "Jindal Steel & Power Limited",
            "CYIENT.NS": "Cyient Limited",
            "JUBLINGREA.NS": "Jubilant Ingrevia Limited",
            "TVSMOTOR.NS": "TVS Motor Company Limited",
            "FIVESTAR.NS": "Five-Star Business Finance Limited",
            "NAUKRI.NS": "Info Edge (India) Limited",
            "MANAPPURAM.NS": "Manappuram Finance Limited",
            "INDUSINDBK.NS": "IndusInd Bank Limited",
            "MEDANTA.NS": "Global Health Limited (Medanta)",
            "TITAGARH.NS": "Titagarh Rail Systems Limited",
            "RADICO.NS": "Radico Khaitan Limited",
            "SJVN.NS": "SJVN Limited",
            "HINDZINC.NS": "Hindustan Zinc Limited",
            "DLF.NS": "DLF Limited",
            "BERGEPAINT.NS": "Berger Paints India Limited",
            "DEVYANI.NS": "Devyani International Limited",
            "M&MFIN.NS": "Mahindra & Mahindra Financial Services Limited",
            "DOMS.NS": "Doms Industries Limited",
            "IOC.NS": "Indian Oil Corporation Limited",
            "SKFINDIA.NS": "SKF India Limited",
            "MUTHOOTFIN.NS": "Muthoot Finance Limited",
            "CENTRALBK.NS": "Central Bank of India",
            "POLYMED.NS": "Poly Medicure Limited",
            "PCBL.NS": "Phillips Carbon Black Limited",
            "BAYERCROP.NS": "Bayer Cropscience Limited",
            "APLLTD.NS": "Alembic Pharmaceuticals Limited",
            "ALKYLAMINE.NS": "Alkyl Amines Chemicals Limited",
            "FACT.NS": "Fertilizers and Chemicals Travancore Limited",
            "TATAELXSI.NS": "Tata Elxsi Limited",
            "TECHNOE.NS": "Techno Electric & Engineering Company Limited",
            "360ONE.NS": "360 ONE WAM Limited",
            "ARE&M.NS": "Amara Raja Energy & Mobility Limited",
            "IDBI.NS": "IDBI Bank Limited",
            "SHYAMMETL.NS": "Shyam Metalics and Energy Limited",
            "CIEINDIA.NS": "CIE Automotive India Limited",
            "CHEMPLASTS.NS": "Chemplast Sanmar Limited",
            "SUZLON.NS": "Suzlon Energy Limited",
            "AUROPHARMA.NS": "Aurobindo Pharma Limited",
            "RENUKA.NS": "Shree Renuka Sugars Limited",
            "CANFINHOME.NS": "Can Fin Homes Limited",
            "APOLLOTYRE.NS": "Apollo Tyres Limited",
            "GRINFRA.NS": "G R Infraprojects Limited",
            "KOTAKBANK.NS": "Kotak Mahindra Bank Limited",
            "ASTRAL.NS": "Astral Limited",
            "CAMS.NS": "Computer Age Management Services Limited",
            "METROBRAND.NS": "Metro Brands Limited",
            "PAGEIND.NS": "Page Industries Limited",
            "CIPLA.NS": "Cipla Limited",
            "TORNTPHARM.NS": "Torrent Pharmaceuticals Limited",
            "SCHAEFFLER.NS": "Schaeffler India Limited",
            "CHALET.NS": "Chalet Hotels Limited",
            "IIFL.NS": "IIFL Finance Limited",
            "EXIDEIND.NS": "Exide Industries Limited",
            "APOLLOHOSP.NS": "Apollo Hospitals Enterprise Limited",
            "AVANTIFEED.NS": "Avanti Feeds Limited",
            "BHARTIARTL.NS": "Bharti Airtel Limited",
            "CDSL.NS": "Central Depository Services (India) Limited",
            "ANGELONE.NS": "Angel One Limited",
            "ABB.NS": "ABB India Limited",
            "MAHABANK.NS": "Bank of Maharashtra",
            "TBOTEK.NS": "TBO Tek Limited",
            "VARROC.NS": "Varroc Engineering Limited",
            "BIRLACORPN.NS": "Birla Corporation Limited",
            "EICHERMOT.NS": "Eicher Motors Limited",
            "CARBORUNIV.NS": "Carborundum Universal Limited",
            "PTCIL.NS": "PTC Industries Limited",
            "NYKAA.NS": "FSN E-Commerce Ventures Limited (Nykaa)",
            "TATASTEEL.NS": "Tata Steel Limited",
            "HONAUT.NS": "Honeywell Automation India Limited",
            "SUNDRMFAST.NS": "Sundram Fasteners Limited",
            "RAILTEL.NS": "RailTel Corporation of India Limited",
            "BHARTIHEXA.NS": "Bharti Hexacom Limited",
            "GODIGIT.NS": "Go Digit General Insurance Limited",
            "SIGNATURE.NS": "Signatureglobal (India) Limited",
            "COLPAL.NS": "Colgate-Palmolive (India) Limited",
            "PATANJALI.NS": "Patanjali Foods Limited",
            "VGUARD.NS": "V-Guard Industries Limited",
            "RAYMOND.NS": "Raymond Limited",
            "M&M.NS": "Mahindra & Mahindra Limited",
            "BATAINDIA.NS": "Bata India Limited",
            "INDIANB.NS": "Indian Bank",
            "ITI.NS": "ITI Limited",
            "YESBANK.NS": "Yes Bank Limited",
            "WESTLIFE.NS": "Westlife Foodworld Limited",
            "TIMKEN.NS": "Timken India Limited",
            "GLAND.NS": "Gland Pharma Limited",
            "SUMICHEM.NS": "Sumitomo Chemical India Limited",
            "NHPC.NS": "NHPC Limited",
            "ZOMATO.NS": "Zomato Limited",
            "GODREJPROP.NS": "Godrej Properties Limited",
            "ASTERDM.NS": "Aster DM Healthcare Limited",
            "CAMPUS.NS": "Campus Activewear Limited",
            "ADANIENT.NS": "Adani Enterprises Limited",
            "NAM-INDIA.NS": "Nippon Life India Asset Management Limited",
            "CAPLIPOINT.NS": "Caplin Point Laboratories Limited",
            "IDFCFIRSTB.NS": "IDFC First Bank Limited",
            "PHOENIXLTD.NS": "The Phoenix Mills Limited",
            "EMCURE.NS": "Emcure Pharmaceuticals Limited",
            "PVRINOX.NS": "PVR INOX Limited",
            "NATIONALUM.NS": "National Aluminium Company Limited",
            "AWL.NS": "Adani Wilmar Limited",
            "INDUSTOWER.NS": "Indus Towers Limited",
            "KANSAINER.NS": "Kansai Nerolac Paints Limited",
            "CHOLAFIN.NS": "Cholamandalam Investment and Finance Company Limited",
            "PPLPHARMA.NS": "Piramal Pharma Limited",
            "PETRONET.NS": "Petronet LNG Limited",
            "BIOCON.NS": "Biocon Limited",
            "FLUOROCHEM.NS": "Gujarat Fluorochemicals Limited",
            "ECLERX.NS": "eClerx Services Limited",
            "VOLTAS.NS": "Voltas Limited",
            "INDGN.NS": "Indigo Paints Limited",
            "CLEAN.NS": "Clean Science and Technology Limited",
            "RATNAMANI.NS": "Ratnamani Metals & Tubes Limited",
            "HCLTECH.NS": "HCL Technologies Limited",
            "ICICIPRULI.NS": "ICICI Prudential Life Insurance Company Limited",
            "PIDILITIND.NS": "Pidilite Industries Limited",
            "ASHOKLEY.NS": "Ashok Leyland Limited",
            "LAURUSLABS.NS": "Laurus Labs Limited",
            "BLS.NS": "BLS International Services Limited",
            "SWANENERGY.NS": "Swan Energy Limited",
            "PFIZER.NS": "Pfizer Limited",
            "RAYMONDLSL.NS": "Raymond Lifestyle Limited",
            "AKUMS.NS": "Akums Drugs & Pharmaceuticals Limited",
            "MSUMI.NS": "Motherson Sumi Wiring India Limited",
            "QUESS.NS": "Quess Corp Limited",
            "BHARATFORG.NS": "Bharat Forge Limited",
            "INDHOTEL.NS": "The Indian Hotels Company Limited",
            "BANDHANBNK.NS": "Bandhan Bank Limited",
            "COROMANDEL.NS": "Coromandel International Limited",
            "JSWENERGY.NS": "JSW Energy Limited",
            "TANLA.NS": "Tanla Platforms Limited",
            "BSOFT.NS": "Birlasoft Limited",
            "SYRMA.NS": "Syrma SGS Technology Limited",
            "SYNGENE.NS": "Syngene International Limited",
            "KPRMILL.NS": "K.P.R. Mill Limited",
            "CENTURYPLY.NS": "Century Plyboards (India) Limited",
            "KAJARIACER.NS": "Kajaria Ceramics Limited",
            "CHENNPETRO.NS": "Chennai Petroleum Corporation Limited",
            "ABREL.NS": "Aditya Birla Real Estate Limited",
            "NUVOCO.NS": "Nuvoco Vistas Corporation Limited",
            "NETWEB.NS": "Netweb Technologies India Limited",
            "SANOFI.NS": "Sanofi India Limited",
            "SAMMAANCAP.NS": "Sammunat Capital Limited",
            "GICRE.NS": "General Insurance Corporation of India",
            "CERA.NS": "Cera Sanitaryware Limited",
            "UJJIVANSFB.NS": "Ujjivan Small Finance Bank Limited",
            "ALOKINDS.NS": "Alok Industries Limited",
            "KSB.NS": "KSB Limited",
            "CEATLTD.NS": "CEAT Limited",
            "ELECON.NS": "Elecon Engineering Company Limited",
            "OLECTRA.NS": "Olectra Greentech Limited",
            "KALYANKJIL.NS": "Kalyan Jewellers India Limited",
            "NSLNISP.NS": "NMDC Steel Limited",
            "DIVISLAB.NS": "Divi's Laboratories Limited",
            "KFINTECH.NS": "KFin Technologies Limited",
            "TATACOMM.NS": "Tata Communications Limited",
            "PGHH.NS": "Procter & Gamble Hygiene and Health Care Limited",
            "INOXINDIA.NS": "INOX India Limited",
            "INOXWIND.NS": "Inox Wind Limited",
            "DRREDDY.NS": "Dr. Reddy's Laboratories Limited",
            "APARINDS.NS": "Apar Industries Limited",
            "MRF.NS": "MRF Limited",
            "GMRAIRPORT.NS": "GMR Airports Infrastructure Limited",
            "SIEMENS.NS": "Siemens Limited",
            "DELHIVERY.NS": "Delhivery Limited",
            "EASEMYTRIP.NS": "Easy Trip Planners Limited",
            "VTL.NS": "Vardhman Textiles Limited",
            "HINDCOPPER.NS": "Hindustan Copper Limited",
            "ABFRL.NS": "Aditya Birla Fashion and Retail Limited",
            "CRAFTSMAN.NS": "Craftsman Automation Limited",
            "VIJAYA.NS": "Vijaya Diagnostic Centre Limited",
            "SCI.NS": "Shipping Corporation of India Limited",
            "ANANTRAJ.NS": "Anant Raj Limited",
            "RBLBANK.NS": "RBL Bank Limited",
            "SONATSOFTW.NS": "Sonata Software Limited",
            "DEEPAKNTR.NS": "Deepak Nitrite Limited",
            "GLAXO.NS": "GlaxoSmithKline Pharmaceuticals Limited",
            "RKFORGE.NS": "Ramkrishna Forgings Limited",
            "USHAMART.NS": "Usha Martin Limited",
            "POONAWALLA.NS": "Poonawalla Fincorp Limited",
            "TORNTPOWER.NS": "Torrent Power Limited",
            "CELLO.NS": "Cello World Limited",
            "NATCOPHARM.NS": "Natco Pharma Limited",
            "KPIL.NS": "Kalpataru Projects International Limited",
            "IRFC.NS": "Indian Railway Finance Corporation Limited",
            "IPCALAB.NS": "Ipca Laboratories Limited",
            "ASAHIINDIA.NS": "Asahi India Glass Limited",
            "HAPPSTMNDS.NS": "Happiest Minds Technologies Limited",
            "RITES.NS": "RITES Limited",
            "FINEORG.NS": "Fine Organic Industries Limited",
            "ENDURANCE.NS": "Endurance Technologies Limited",
            "BALKRISIND.NS": "Balkrishna Industries Limited",
            "GODREJAGRO.NS": "Godrej Agrovet Limited",
            "TATATECH.NS": "Tata Technologies Limited",
            "BLUEDART.NS": "Blue Dart Express Limited",
            "ALKEM.NS": "Alkem Laboratories Limited",
            "SUNPHARMA.NS": "Sun Pharmaceutical Industries Limited",
            "IDEA.NS": "Vodafone Idea Limited",
            "MASTEK.NS": "Mastek Limited",
            "JBMA.NS": "JBM Auto Limited",
            "ZENSARTECH.NS": "Zensar Technologies Limited",
            "INTELLECT.NS": "Intellect Design Arena Limited",
            "GRINDWELL.NS": "Grindwell Norton Limited",
            "RVNL.NS": "Rail Vikas Nigam Limited",
            "HONASA.NS": "Honasa Consumer Limited",
            "UNOMINDA.NS": "UNO Minda Limited",
            "IOB.NS": "Indian Overseas Bank",
            "JSL.NS": "Jindal Stainless Limited",
            "KNRCON.NS": "KNR Constructions Limited",
            "JMFINANCIL.NS": "JM Financial Limited",
            "GRAPHITE.NS": "Graphite India Limited",
            "MINDACORP.NS": "Minda Corporation Limited",
            "ZYDUSLIFE.NS": "Zydus Lifesciences Limited",
            "BALAMINES.NS": "Balaji Amines Limited",
            "NUVAMA.NS": "Nuvama Wealth Management Limited",
            "LUPIN.NS": "Lupin Limited",
            "KPITTECH.NS": "KPIT Technologies Limited",
            "MRPL.NS": "Mangalore Refinery and Petrochemicals Limited",
            "TRITURBINE.NS": "Triveni Turbine Limited",
            "SUNDARMFIN.NS": "Sundaram Finance Limited",
            "CROMPTON.NS": "Crompton Greaves Consumer Electricals Limited",
            "SUVENPHAR.NS": "Suven Pharmaceuticals Limited",
            "BAJAJHLDNG.NS": "Bajaj Holdings & Investment Limited",
            "MOTHERSON.NS": "Samvardhana Motherson International Limited",
            "HEG.NS": "HEG Limited",
            "GRANULES.NS": "Granules India Limited",
            "RAJESHEXPO.NS": "Rajesh Exports Limited",
            "AUBANK.NS": "AU Small Finance Bank Limited",
            "AJANTPHARM.NS": "Ajanta Pharma Limited",
            "TATAMOTORS.NS": "Tata Motors Limited",
            "SONACOMS.NS": "Sona BLW Precision Forgings Limited",
            "JBCHEPHARM.NS": "JB Chemicals & Pharmaceuticals Limited"

    }

def to_crores(x):
    """Convert numbers to Crores (Indian numbering system)"""
    return x / 10000000

def fetch_stock_data(ticker):
    """Fetch comprehensive stock data from Yahoo Finance"""
    try:
        stock = yf.Ticker(ticker)
        info = stock.info or {}
        hist = stock.history(period="max")
        
        if hist.empty:
            raise ValueError("No historical data available")
            
        # Remove timezone if present
        if hist.index.tz is not None:
            hist.index = hist.index.tz_localize(None)
            
        return {
            'info': info,
            'hist': hist,
            'financials': stock.financials,
            'balance_sheet': stock.balance_sheet,
            'cashflow': stock.cashflow,
            'quarterly_financials': stock.quarterly_financials,
            'quarterly_balance_sheet': stock.quarterly_balance_sheet,
            'quarterly_cashflow': stock.quarterly_cashflow
        }
    except Exception as e:
        st.error(f"Failed to fetch data for {ticker}: {str(e)}")
        return None

# SIDEBAR - STOCK SELECTION 
with st.sidebar:
    st.markdown(f"""
    <h2 style='color: {COLORS["text_primary"]};'>
        🔍 Stock Search
    </h2>
    """, unsafe_allow_html=True)
    
    STOCK_DB = get_indian_stocks()
    search_term = st.text_input(
        "Enter stock symbol or company name",
        placeholder="RELIANCE.NS or Reliance"
    ).upper()
    
    ticker = None
    if search_term:
        matches = [f"{symbol} - {name}" for symbol, name in STOCK_DB.items() 
                  if search_term in symbol or search_term in name.upper()]
        
        if matches:
            selected = st.selectbox("Select stock", matches)
            ticker = selected.split(" - ")[0]
        else:
            st.warning("No matching stocks found. Try: RELIANCE.NS, TATASTEEL.NS")

#  MAIN DASHBOARD 
st.markdown(f"""
<h1 style='color: {COLORS["text_primary"]};'>
    📊 EquityX - Stock Analysis Dashboard
</h1>
""", unsafe_allow_html=True)

if not ticker:
    # Welcome message when no stock is selected
    st.markdown(f"""
    <div style="background-color: {COLORS['bg_card']}; 
                padding: 1.5rem; 
                border-radius: 0.5rem;
                border-left: 4px solid {COLORS['accent_primary']};
                color: {COLORS['text_primary']}">
        <strong>Welcome to EquityX 🔍</strong>
        <br><br>
        👈 Please select a stock from the sidebar to begin analysis.
        <br><br>
        <strong>Popular Indian Stocks:</strong>
        <ul>
            <li>RELIANCE.NS (Reliance Industries)</li>
            <li>HDFCBANK.NS (HDFC Bank)</li>
            <li>TCS.NS (Tata Consultancy Services)</li>
            <li>INFY.NS (Infosys)</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# Fetch and validate stock data
stock_data = fetch_stock_data(ticker)
if stock_data is None:
    st.error("Failed to load stock data. Please try another stock or check your connection.")
    st.stop()

info = stock_data['info']
hist = stock_data['hist']

# TECHNICAL ANALYSIS SECTION 
st.markdown(f"""
<h2 style='color: {COLORS["text_primary"]};'>
    Technical Analysis
</h2>
""", unsafe_allow_html=True)

# Date range 
col1, col2 = st.columns(2)
with col1:
    start_date = st.date_input("From", value=datetime.now() - timedelta(days=365))
with col2:
    end_date = st.date_input("To", value=datetime.now())

# Current price display
current_price = info.get('currentPrice') or info.get('regularMarketPrice')
st.metric(
    "Current Price", 
    f"₹{current_price:,.2f}" if current_price else "N/A",
    delta=f"{info.get('regularMarketChangePercent', 0):.2f}%" if 'regularMarketChangePercent' in info else None
)

# Filter historical data by date range
start_dt = datetime.combine(start_date, datetime.min.time())
end_dt = datetime.combine(end_date, datetime.min.time())
range_hist = hist[(hist.index >= start_dt) & (hist.index <= end_dt)]

if not range_hist.empty:
    # Calculate moving averages
    range_hist['50MA'] = range_hist['Close'].rolling(50).mean()
    range_hist['200MA'] = range_hist['Close'].rolling(200).mean()
    
    # Create interactive price chart
    fig = px.line(
        range_hist, 
        x=range_hist.index, 
        y=['Close', '50MA', '200MA'],
        title=f"{info.get('shortName', ticker)} Price Movement",
        labels={'value': 'Price (₹)', 'variable': 'Metric'},
        color_discrete_map={
            'Close': COLORS['chart_line'],
            '50MA': COLORS['chart_ma50'],
            '200MA': COLORS['chart_ma200']
        }
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Technical indicators summary
    st.subheader("Key Technical Indicators")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("50-Day MA", f"₹{range_hist['50MA'].iloc[-1]:,.2f}" if not pd.isna(range_hist['50MA'].iloc[-1]) else "N/A")
    with col2:
        st.metric("200-Day MA", f"₹{range_hist['200MA'].iloc[-1]:,.2f}" if not pd.isna(range_hist['200MA'].iloc[-1]) else "N/A")
    with col3:
        if not pd.isna(range_hist['50MA'].iloc[-1]) and not pd.isna(range_hist['200MA'].iloc[-1]):
            crossover = "Bullish" if range_hist['50MA'].iloc[-1] > range_hist['200MA'].iloc[-1] else "Bearish"
            st.metric("MA Crossover", crossover)

# ANALYSIS TABS 
tab1, tab2, tab3 = st.tabs(["📈 Overview", "💹 Financials", "📊 Valuation"])

with tab1:  # Company Overview
    st.markdown(f"""
    <h2 style='color: {COLORS["text_primary"]};'>
        {info.get('longName', STOCK_DB.get(ticker, ticker))} ({ticker})
    </h2>
    """, unsafe_allow_html=True)
    
    # Key metrics in columns
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Market Cap", f"₹{info.get('marketCap', 0)/1e7:,.0f} Cr" if info.get('marketCap') else "N/A")
        st.metric("Sector", info.get('sector', 'N/A'))
    with col2:
        st.metric("52W High", f"₹{info.get('fiftyTwoWeekHigh', 'N/A'):,.2f}")
        st.metric("52W Low", f"₹{info.get('fiftyTwoWeekLow', 'N/A'):,.2f}")
    with col3:
        st.metric("Volume", f"{info.get('volume', 'N/A'):,}" if isinstance(info.get('volume'), int) else "N/A")
        st.metric("Avg. Volume", f"{info.get('averageVolume', 'N/A'):,}" if isinstance(info.get('averageVolume'), int) else "N/A")
    
    # Business summary
    st.subheader("Business Summary")
    st.write(info.get('longBusinessSummary', 'No business description available.'))

with tab2:  # Financials
    st.header("Financial Analysis (₹ Crores)")
    
    period = st.radio("Period:", ["Annual", "Quarterly"], horizontal=True)
    financials = stock_data['quarterly_financials'] if period == "Quarterly" else stock_data['financials']
    cashflow = stock_data['quarterly_cashflow'] if period == "Quarterly" else stock_data['cashflow']
    
    if not financials.empty:
        st.subheader("Income Statement")
        financials_cr = financials.apply(to_crores)
        st.dataframe(
            financials_cr.style.format("{:,.2f} Cr")
            .applymap(lambda x: f"color: {COLORS['accent_success']}" if isinstance(x, (int, float)) and x > 0 
                      else f"color: {COLORS['accent_danger']}" if isinstance(x, (int, float)) and x < 0 
                      else "")
        )
    
    if not cashflow.empty:
        st.subheader("Cash Flow Statement")
        cashflow_cr = cashflow.apply(to_crores)
        st.dataframe(
            cashflow_cr.style.format("{:,.2f} Cr")
            .applymap(lambda x: f"color: {COLORS['accent_success']}" if isinstance(x, (int, float)) and x > 0 
                      else f"color: {COLORS['accent_danger']}" if isinstance(x, (int, float)) and x < 0 
                      else "")
        )

with tab3:  # Valuation
    st.header("Valuation Metrics")
    
    # Valuation Ratios
    valuation_data = {
        "Metric": ["P/E", "P/B", "P/S", "EV/EBITDA", "Dividend Yield"],
        "Value": [
            info.get('trailingPE', 'N/A'),
            info.get('priceToBook', 'N/A'),
            info.get('priceToSalesTrailing12Months', 'N/A'),
            info.get('enterpriseToEbitda', 'N/A'),
            f"{info.get('dividendYield', 0)*100:.2f}%" if info.get('dividendYield') else "N/A"
        ]
    }
    st.dataframe(pd.DataFrame(valuation_data), hide_index=True)
    
    # Profitability Ratios
    profitability_data = {
        "Metric": ["ROE", "ROA", "Operating Margin", "Gross Margin"],
        "Value": [
            f"{info.get('returnOnEquity', 0)*100:.2f}%" if info.get('returnOnEquity') else "N/A",
            f"{info.get('returnOnAssets', 0)*100:.2f}%" if info.get('returnOnAssets') else "N/A",
            f"{info.get('operatingMargins', 0)*100:.2f}%" if info.get('operatingMargins') else "N/A",
            f"{info.get('grossMargins', 0)*100:.2f}%" if info.get('grossMargins') else "N/A"
        ]
    }
    st.dataframe(pd.DataFrame(profitability_data), hide_index=True)

# FOOTER 
st.divider()
st.markdown(f"""
<div style="color: {COLORS['text_secondary']}; font-size: 0.9em;">
    <strong>Data Source:</strong> Yahoo Finance 
</div>
""", unsafe_allow_html=True)

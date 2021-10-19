mkdir -p ~/.streamlit/

echo "[theme]\n\
primaryColor='#F63366'\n\
backgroundColor='#FFFFFF'\n\
secondaryBackgroundColor='#F0F2F6'\n\
textColor='#262730'\n\
font='sans serif'\n\
[server]\n\
headless = true\n\
enableCORS=false\n\
port = $PORT\n\
" > ~/.streamlit/config.toml
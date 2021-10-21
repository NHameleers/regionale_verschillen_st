mkdir -p ~/.streamlit/

echo "[theme]\n\
primaryColor='#F63366'\n\
backgroundColor='#FFFFFF'\n\
secondaryBackgroundColor='#F0F2F6'\n\
textColor='#262730'\n\
font='sans serif'\n\
[server]\n\
port = $PORT\n\
enableCORS = false\n\
headless = true\n\
\n\
" > ~/.streamlit/config.toml